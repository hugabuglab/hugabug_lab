---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# <i class="fas fa-users"></i>Team

<!-- {% include section.html %} -->

{%
  include list.html
  data="members"
  component="portrait"
%}
{:.center}

{% include section.html %}

# <i class="fas fa-users"></i>Join

#### We welcome project workers with any level of experience

Bachelor and master students who combine a biological background with basic programming skills are always welcome to apply. Inquiries by email.

{% include section.html %}

# Funding

Our work is made possible by funding from The Knut and Alice Wallenberg Foundation through the Data-Driven Life Sciences fellows programme.
{:.left}

{%
  include gallery.html
  style="square"

  image1="images/kaw.jpg"
  link1="https://kaw.wallenberg.org/en"
  tooltip1="KAW Foundation"

  image2="images/scilifelab.jpg"
  link2="https://www.scilifelab.se/data-driven/"
  tooltip2="SciLifeLab"

%}
