variable "node_count" {
  type = number
  default = 1
}

variable "region" {
  type        = string
  description = "An example variable that can only be 'value1' or 'value2'."

  validation {
    condition     = var.region == "us-east1" || var.region == "southamerica-east1"
    error_message = "The example_variable must be either 'value1' or 'value2'."
  }
  default = "us-east1"
}

