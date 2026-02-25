terraform {
  required_version = ">= 1.3.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = ">= 3.2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.4.0"
    }
  }
}

variable "provisioning_units" {
  type        = number
  description = "Represents standardized provisioning units (e.g., tenant baseline + workload patterns)."
  default     = 12
}

resource "random_id" "run" {
  byte_length = 4
}

resource "null_resource" "provision_units" {
  triggers = {
    run_id            = random_id.run.hex
    provisioning_units = tostring(var.provisioning_units)
  }
}

resource "local_file" "change_plan" {
  filename = "${path.module}/_generated_plan_${random_id.run.hex}.txt"
  content  = <<EOT
OKML Local Terraform Model

Run: ${random_id.run.hex}
Provisioning units: ${var.provisioning_units}

This config intentionally models "provisioning units" locally and is safe to run without infrastructure.
EOT
}

output "provisioning_units" {
  value = var.provisioning_units
}

output "standardized_k8s_baseline" {
  value = true
}

