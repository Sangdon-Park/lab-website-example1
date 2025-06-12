---
title: Projects
nav:
  order: 2
  tooltip: Research Projects & Models
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

Our research projects focus on developing advanced climate models and analyzing complex Earth system interactions. We combine computational modeling with observational data to understand climate dynamics and their implications for environmental management and policy.

{% include tags.html tags="climate modeling, carbon cycle, fire dynamics, earth system" %}

{% include search-info.html %}

{% include section.html %}

## Featured

{% include list.html component="card" data="projects" filter="group == 'featured'" %}

{% include section.html %}

## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
