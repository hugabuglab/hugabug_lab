---
title: News & Updates
nav:
  order: 4
  tooltip: Latest news and updates from the lab
description: "Stay up to date with the latest research, achievements, and news from The Human Molecular Ecology Lab. Discover our groundbreaking work in gut microbiome research and maternal health."
keywords: "lab news, research updates, microbiome research, maternal health, scientific achievements"
---

# {{ page.title }}

<div class="blog-intro">
  <p class="lead">
    Welcome to our news and updates section! Here you'll find the latest developments from our research team, 
    including breakthrough discoveries, team achievements, and insights into our work on the human microbiome 
    and its impact on health and disease.
  </p>
</div>

{% include post-list.html %}

<!-- Additional Features Section -->
<div class="blog-features">
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon">📊</div>
      <h3>Research Highlights</h3>
      <p>Discover our latest findings and their implications for human health and microbiome science.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">👥</div>
      <h3>Team Achievements</h3>
      <p>Celebrate the accomplishments and milestones of our talented research team members.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🔬</div>
      <h3>Scientific Insights</h3>
      <p>Explore the science behind our research and its potential applications in healthcare.</p>
    </div>
  </div>
</div>

<style>
  .blog-intro {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px;
    background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%);
    border-radius: 15px;
    border-left: 5px solid #03a9f4;
  }

  .lead {
    font-size: 1.2rem;
    color: #01579b;
    line-height: 1.7;
    margin: 0;
    font-weight: 400;
  }

  .blog-features {
    margin-top: 60px;
    padding: 40px 0;
    background: #f5f5f5;
    border-radius: 20px;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .feature-card {
    text-align: center;
    padding: 30px 20px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-top: 4px solid #03a9f4;
  }

  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: 20px;
    display: block;
  }

  .feature-card h3 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #01579b;
    margin-bottom: 15px;
    font-family: 'Montserrat', sans-serif;
  }

  .feature-card p {
    color: #424242;
    line-height: 1.6;
    margin: 0;
  }

  @media (max-width: 768px) {
    .blog-intro {
      padding: 20px;
      margin-bottom: 30px;
    }

    .lead {
      font-size: 1.1rem;
    }

    .features-grid {
      grid-template-columns: 1fr;
      gap: 20px;
      padding: 0 15px;
    }

    .feature-card {
      padding: 25px 15px;
    }
  }
</style>
