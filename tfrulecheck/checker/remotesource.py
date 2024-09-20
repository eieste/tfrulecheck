from tofudecorator.checker.base import BaseChecker, HclBlock
# from tofudecorator.checker.base import


class RemoteSourceChecker(BaseChecker):
    name = "forcedremotesource"
    checker_id = "TF1"
    applied_to = [HclBlock.ALL]

    def handle(self, block_type, block):
        if self.match_decorator(block):
            module_block = list(block.values())[0]

            if not module_block.get("version"):
                self.log.error("Module Block had no Version Defined")
                self.ctrl.
            
            if module_block.get("source")[0] == ".":
                self.log.error("Module Block has no Remote Source")
                