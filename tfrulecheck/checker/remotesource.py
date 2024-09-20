from tfrulecheck.checker.base import BaseChecker, HclBlock


class RemoteSourceChecker(BaseChecker):
    name = "forcedremotesource"
    checker_id = "TF1"
    applied_to = [HclBlock.ALL]

    def handle(self, block_type, block):

        if self.match_decorator(block):
            module_block = list(block.values())[0]

            if not module_block.get("version"):
                self.log.error("Module Block had no Version Defined", extra={"checker_id": self.get_checker_id()})
                self.ctrl.set_error_state()
            
            if module_block.get("source")[0] == ".":
                self.log.error("Module Block has no Remote Source", extra={"checker_id": self.get_checker_id()})
                self.ctrl.set_error_state()
                