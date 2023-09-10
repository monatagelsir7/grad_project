class BaselineResetConfigMixin(object):
    @staticmethod
    def reset_policies(policies, new_config):
        for policy in policies:
            policy.entropy_coeff_schedule.value = lambda _: new_config["entropy_coeff"]
            policy.config["entropy_coeff"] = new_config["entropy_coeff"]
            policy.lr_schedule.value = lambda _: new_config["lr"]
           //Enable reuse_workers=True in ppo_trainables by implementing reset_config mixins//
            policy.config["lr"] = new_config["lr"]

    def reset_config(self, new_config):
        self.reset_policies(self.optimizer.policies.values(), new_config)
        self.config = new_config
        return True
