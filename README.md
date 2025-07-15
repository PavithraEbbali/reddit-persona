# 🧠 Reddit User Persona Generator

This script analyzes a Reddit user's posts and comments to generate a detailed **user persona**, including **citations** from their activity.

## 📌 Features

- Scrapes a Reddit user’s **posts** and **comments**
- Uses content to generate a detailed **user persona**
- Cites specific **comments/posts** used for each characteristic
- Outputs result as a `.txt` file
- Compliant with **PEP-8 guidelines**
- Easy to run
  
---

## 🧰 Technologies Used

- Python 3.8+
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/)
- [OpenAI GPT API](https://platform.openai.com/docs/)
- `dotenv`, `requests`, `tqdm`, `logging`

---

## 🛠️ Full Setup Instructions (Step-by-Step)

Follow these steps to set up and run the Reddit User Persona Generator on your local system.

### ✅ Prerequisites

- Python 3.8 or higher
- Git installed
- An [OpenAI API Key](https://platform.openai.com/account/api-keys)
- A Reddit App (to get your Reddit `client_id`, `client_secret`, and `user_agent`):
  - Go to: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
  - Click **"create app"**
  - Choose type: **script**
  - Fill in name, description, and a dummy redirect URI like `http://localhost`
  - Save to get your credentials

---

### 📁 Step 1: Clone the GitHub Repository

```bash
git clone https://github.com/PavithraEbbali/reddit-persona.git
cd reddit-persona
```

---

### 📦 Step 2: Install Required Dependencies

Use pip to install all packages from the `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

### 🔐 Step 3: Create a `.env` File

Create a `.env` file in the root of the project:

```bash
touch .env
```

Then open the `.env` file in your editor and paste your credentials:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_app_name
OPENAI_API_KEY=your_openai_api_key
```
---

### ▶️ Step 4: Run the Script

To start the Reddit persona generator:

```bash
python main.py
```

When prompted, enter a Reddit profile URL, for example:

```ruby
https://www.reddit.com/user/kojied/
https://www.reddit.com/user/Hungry-Move-6603/ 
```

---

### 📂 Step 5: View the Output

After processing, the output will be saved in the `output/` folder as:

```lua
output/<username>_raw_<YYYYMMDD_HHMMSS>.txt
```






