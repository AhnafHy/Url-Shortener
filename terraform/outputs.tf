output "api_url" {
  value       = aws_api_gateway_stage.prod.invoke_url
  description = "Base URL for the URL shortener API"
}