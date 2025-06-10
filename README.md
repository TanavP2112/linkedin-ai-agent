Welcome to LinkedBot! The one stop chatbot that will land your future dream job! whether it's a giant FAANG company or a rising startup in need of exceptional talendt, LinkedBot is here to help you land that job!

# Features

- **Resume Judger**: Get instant feedback on your resume to make it stand out.
- **Job Search**: Find job listings tailored to your skills and preferences.
- **AI Preview**: Preview your resume from the eyes of an AI recruiter. Figure out if your resume is parsing correctly.

If you want tailored advice, make sure to upload your resume and provide your LinkedIn profile URL. The AI will use this information to give you the best possible advice. However, the AI is limited due to LinkedIn's API restrictions, so it may not be able to access everything. Web scraping could be a future option, but it is not currently implemented in its current state.

and old agent folder is still available for reference, as it was my initial starting point before I switched to attempting to host the application on Render + Streamlit Cloud.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Hosting**: Render.com

This robust stack is ideal for protoyping AI agents and getting an MVP up and running as fast as possible. For larger scaled applications, I would consider using a framework such as Next.js + React, along with PostgreSQL for the database and Redis for caching. In terms of routing, Tanstack Router is a great choice for Next.js applications. No complex algorithms were necessary for this mini-project, as most of the heavy lifting is done by the Gemini API and the streamlit functions.

Note: The deployment is currently bugged, feel free to run the code locally using the instructions below.

## Running Locally

run the following commands to set up the environment and start the application:
`pip install -r requirements.txt`

`streamlit run app.py`

make sure to then set the environment variables for the Gemini API key by creating a `.env` file in the root directory with the following content:
`GEMINI_API_KEY=[your_api_key_here]`

## Questions or Concerns

Feel free to reach out about any questions or concerns you may have. You can contact me at tanavp2@illinois.edu.
