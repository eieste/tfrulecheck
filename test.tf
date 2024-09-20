resource "foo" "bar" {
    test = "abc"

    another {

    }

}

module "thisistanexample" {
    source = "../../../"
}

# @forcedremotesource
module "thisistananotherexample" {
    source = "git@gitlab.com"
    version = "1.2.3"
}

module "thisistanotherexample" {
    source = "../../../"
}

