class User:
    def __init__(self, user_id, user_name, user_req={}):
        self.user_id = user_id
        self.user_name = user_name
        self.user_req = user_req

    def action_add_iter(self, action_name):
        if not self.user_req:
            self.user_req[action_name] = 1
        else:
            if action_name in self.user_req:
                self.user_req[action_name] += 1
            else:
                self.user_req[action_name] = 1

    def get_action_value(self, action_name):
        action_value = 0
        if action_name == 'all':
            for key in self.user_req.keys():
                action_value += self.user_req[key]
        else:
            if action_name in self.user_req:
                action_value = self.user_req[action_name]
        return action_value

