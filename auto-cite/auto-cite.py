import sys
import os

# Get absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from util import log, load_data, cite_with_manubot
from importlib import import_module
from dict_hash import sha256
import yaml

# Debug logging
log(f"Project root: {PROJECT_ROOT}", 2)

# config info for input/output files and plugins
config = {}
try:
    config_path = os.path.join(PROJECT_ROOT, "_config.yaml")
    log(f"Looking for config at: {config_path}", 2)
    
    config = load_data(config_path, type_check=False).get("auto-cite")
    if not config:
        raise Exception("Couldn't find auto-cite key in config")
except Exception as message:
    log(message, 3, "red")
    exit(1)

log("Compiling list of sources to cite")

# compile master list of sources from various plugins
sources = []

# loop through plugins
for plugin in config.get("plugins", []):
    # get plugin props
    name = plugin.get("name", "-")
    files = plugin.get("input", "")

    # show progress
    log(f"Running {name} plugin")

    # loop through plugin input files
    for file in files:
        # Convert to absolute path
        abs_file = os.path.join(PROJECT_ROOT, file)
        log(f"Looking for file at: {abs_file}", 2)

        # show progress
        log(file, 2)

        # get data in file
        data = []
        try:
            data = load_data(abs_file)
        except Exception as message:
            log(f"Error loading file {abs_file}: {message}", 3, "red")
            exit(1)

        # run plugin
        plugin_sources = import_module(f"plugins.{name}").main(data)

        log(f"Got {len(plugin_sources)} sources", 2, "green")

        for source in plugin_sources:
            # make unique key for cache matching
            source["_cache"] = sha256({**source, "plugin": name, "input": file})
            # add source
            sources.append(source)

log("Generating citations for sources")

# Initialize citations list
citations = []

log("GENERATING CITATIONS FOR SOURCES")

# Loop through sources and generate citations
for index, source in enumerate(sources):
    log(f"Source {index + 1} of {len(sources)} - {source.get('id', '-')}")
    
    try:
        # Generate citation using Manubot
        log("Using Manubot to generate new citation", 2)
        citation = cite_with_manubot(source)
        
        # Add source metadata to citation
        citation.update(
            {key: value for key, value in source.items() if not key.startswith("_")}
        )
        
        # Add citation to list
        citations.append(citation)
        log(f"Added citation for {source.get('id', '-')}", 2, "green")
        
    except Exception as e:
        log(f"Error generating citation for {source.get('id', '-')}: {e}", 3, "red")
        continue

log("EXPORTING CITATIONS")

# Get output path from config
output_file = config.get("output", "_data/citations.yaml")
output_path = os.path.join(PROJECT_ROOT, output_file)

try:
    # Create _data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Add header comment to citations file
    header = "# DO NOT EDIT, GENERATED AUTOMATICALLY FROM SOURCES.YAML (AND ELSEWHERE)\n"
    header += "# See https://github.com/greenelab/lab-website-template/wiki/Citations\n\n"
    
    # Write citations to file
    with open(output_path, 'w') as f:
        f.write(header)
        yaml.dump(citations, f, default_flow_style=False, sort_keys=False)
    
    log(f"Successfully wrote {len(citations)} citations to {output_path}", 2, "green")
except Exception as e:
    log(f"Error writing citations to {output_path}: {e}", 3, "red")
    exit(1)
