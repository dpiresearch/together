# Sketch to Code

Will read an image file that outlines a workflow and try to write code based on what it sees
Preso: https://docs.google.com/presentation/d/1IfpRbCfkWnNqwWTjSevx2tLyMhqbwnJ-/edit?usp=sharing&ouid=109164369295310357886&rtpof=true&sd=true

## Outline

Code sends an image to GPT-4 to get a summary.  Using that summary, it goes to another LLM to get code.  If it works, the code will run.

## Tech Stack

OpenAI (GPT-4V)
Mixtral 8x7B ( Together ai )
