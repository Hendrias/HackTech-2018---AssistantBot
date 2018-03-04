# Slackbot-Tutorial
A tutorial on how to make a Slackbot in Python


## Setup
#### Install Python
First make sure you have some version of Python installed. You can do this by going [here](https://www.python.org/downloads/).

#### Install pip
Next make sure you have `pip` (a python package manager) installed, by typing `pip` into your terminal. If you do not have it installed,
you can install it by going [here](https://pip.pypa.io/en/stable/installing/).

#### Install slackclient
Finally, you'll need to install `slackclient` a Python library for interfacing with the Slack API. Run the below command in your terminal to install it.

```
pip install slackclient
```
#### Setup Slack Workspace
Next head over [here](https://slack.com/create) to create a Slack workspace to set your bot up in. Go through the sign up flow for making an account
and workspace.

#### Setup Slack App and Bot Integration
Once you finish making a workspace, go [here](https://api.slack.com/apps) and click create new app.

![Create New App](img/create_app.png)

Once you've created the app, fill out the basic information on the bottom of the `Basic Information` section. Then, you'll need to add a bot user to the app so users can converse with it. On the left toolbar, click `Bot Users`, fill in the details, and hit add bot.

Now you'll be able to install the app to your workspace. On the left toolbar, hit `Install App` and follow the flow to add the app to your workspace. Once completed, you should be able to see your OAuth tokens when are in the `Install App` section of the toolbar.

Now you visit your Slack in a new tab at `https://yourslack.slack.com` you should be able to see your app under the Apps header in the left toolbar.

#### Run the bot locally
Clone this repository.

Head back to the admin section and create a file in your project directory called `config.py` and copy the `Bot User OAuth Access Token` on the `Install App` page into a variable like this:

```
BOT_ACCESS_TOKEN = "xoxb-..."
```

Go to your terminal, navigate to the project repository and run the command

```
python bot.py
```

This will start the bot and you should see a corresponding message in your terminal indicating this. Navigate back to your Slack and DM the bot. If you DM it `hello` it should respond with `hello there`. You can add the bot to any channel you want and it will start monitoring messages in that channel.

## Expanding Functionality

#### Slack API
Head over [here](https://api.slack.com/methods) to see all the possible methods you can use. Click on each method to see what arguements and permission scope it requires.

When you find a method in the API you want to use, you can add it to your code in the following way. Consider the API method `channels.info` [here](https://api.slack.com/methods/channels.info) that gives a list of channels in the Slack. These are the arguments listed on the API page.

![channels.info arguments](img/channels_info.png)

We can make the call from inside our SlackBot class in our code by creating a method like this:

```
def get_channel_info(self, channel):
	res = self.sc.api_call("channel.info", channel=channel)
	return res
```
Any API call you want to make, you can simple use `sc.api_call` and just provide it with the API method as well as values for at least all required arguments.

Here are some of the other things you can add to your Slack bot (all setup details found in the admin panel of your Slack):

![extra functionality](img/extras.png)


Happy hacking!
