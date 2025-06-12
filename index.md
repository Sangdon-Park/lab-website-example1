---
title: Home
nav:
  order: 0
  tooltip: KAIST Climate System Lab
---

# KAIST Climate System Lab

{% capture col1 %}
{%
  include figure.html
  image="images/lab-main-photo.jpg"
  caption=""
  width="100%"
%}
{% endcapture %}

{% capture col2 %}
## 🌍 Understanding Earth's Climate System

기후 변화는 인류가 직면한 가장 큰 위협 중 하나입니다. 지구온난화 외에도 극한 기상 현상의 강도/빈도 증가와 기후 시스템의 변화는 생태계, 건강, 식량 안보, 경제, 사회에 다양한 영향을 미치고 있습니다.

*Climate change is one of the greatest threats facing humanity. Beyond global warming, increasing intensity and frequency of extreme weather events and changes in climate systems are impacting ecosystems, health, food security, economy, and society in various ways.*

### Our Mission
We advance understanding of Earth's complex climate system through **interdisciplinary research**, **advanced modeling**, and **data-driven analysis**. Our work bridges fundamental climate science with practical solutions for climate adaptation and mitigation.
{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

{%
  include button.html
  link="research"
  text="Our Research"
  icon="fa-solid fa-microscope"
%}
{%
  include button.html
  link="mailto:jinddu@gmail.com"
  text="Contact Us"
  icon="fa-solid fa-envelope"
%}

{% include section.html %}

## Highlights

{% capture text %}

🔬 **Climate System Science**: Understanding complex linkages like cold surge ↔ frost damage, snow ↔ fire interactions, and stomata behavior ↔ Arctic warming patterns.

🌊 **Earth System Modeling**: Predicting future climate states through integrated environmental sub-system analysis.

🌱 **Carbon-Climate Feedback**: Investigating how climate change impacts the global carbon cycle - crucial for achieving carbon neutrality by 2050.

🔥 **Fire-Climate Interactions**: Studying regional fire dynamics and their relationship with changing atmospheric conditions.

{%
  include button.html
  link="research"
  text="Explore our research"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/research-diagram-1.jpg"
  link="research"
  title="Climate System Science"
  text=text
%}

{% capture text %}

**🌍 Current Research Highlights:**

📊 **Carbon-Climate Feedback Analysis** - Understanding how land and ocean systems absorb ~50% of carbon emissions and predicting future changes

🌲 **Siberian Fire Dynamics** - Discovering how earlier snow melting leads to large-scale fire activity in southeastern Siberia  

🌡️ **Temperature-Precipitation Coupling** - Analyzing seasonal variations in sea surface temperature sensitivity across regions

💻 **Advanced Climate Modeling** - Using cutting-edge computational models to predict Earth system responses to climate change

{%
  include button.html
  link="projects"
  text="View all projects"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/research-diagram-2.jpg"
  link="projects"
  title="Research Projects"
  flip=true
  style="bare"
  text=text
%}

{% capture text %}

**👨‍🔬 Led by Prof. Jin-Soo Kim** (KAIST, formerly City University of Hong Kong, University of Zurich)

**🌟 Our International Team:**
- 3 **Postdoctoral Researchers** - Urban climate, Arctic systems, biogeochemical cycles
- 4 **PhD Students** - Climate economics, blue carbon, fire-climate interactions, remote sensing
- **Alumni** now at leading institutions (Yonsei University, etc.)

**🎓 Currently Recruiting:** Master's students (우선 모집), PhD students, and postdoctoral researchers

*"사랑할 줄 알고 사랑받을 줄 아는 사람, 성숙한 사람, 실수를 인정할 수 있는 사람"* - Our lab philosophy

{%
  include button.html
  link="team"
  text="Join our team"
  icon="fa-solid fa-users"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/pi_insights_pi_insights_image_2.jpg"
  link="team"
  title="Our Team"
  text=text
%}
