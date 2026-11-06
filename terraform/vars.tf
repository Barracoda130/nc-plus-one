

variable "github_token" {
  type      = string
  sensitive = true
  default   = ""
}

variable "app_commit_sha" {
  type    = string
  default = ""
}
