def send_email(self,user_emails):
        store = self.sc.api_call("users.list")

        user_emails = []
        for users in store["members"]:
            if "email" in users["profile"]:
                print(users["profile"]["email"])
                user_emails.append(users["profile"]["email"])
                
        return user_emails
