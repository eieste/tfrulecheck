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
    source = "../"
    version = "1.2.3"
}

module "thisistanotherexample" {
    source = "../../../"
}

