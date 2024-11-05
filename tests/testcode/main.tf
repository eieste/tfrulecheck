terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  alias   = "user"
  region  = var.region
  profile = var.profile
}
resource "aws_s3_bucket" "example" {
  provider      = aws.user
  bucket        = var.bucket_name
  acl           = var.acl_value
  force_destroy = "false"           # Will prevent destruction of bucket with contents inside
}

resource "aws_s3_bucket_object" "object2" {
  for_each = fileset("myfiles/", "*")
  bucket   = aws_s3_bucket.example.bucket
  key      = "new_objects"
  source   = "myfiles/${each.value}"
  etag     = filemd5("myfiles/${each.value}")
}



# @forcedremotesource
module "testmodule_localsource" {
  source = "../../"

}

# @forcedremotesource
module "testmodule_remotesource" {
  source = "git@github.com"
  version = "1.2.3"
}

# @moveddate(create="01-11-2024", expire="02-11-2024")
moved {
  from = "old"
  to   = "new"
}
