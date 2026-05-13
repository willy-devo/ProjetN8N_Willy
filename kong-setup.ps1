# kong-setup.ps1
$KONG = "http://localhost:8001"

# Lire la clé Mistral depuis .env
$MISTRAL_KEY = (Get-Content .env | Where-Object { $_ -match "^MISTRAL_API_KEY=" }) -replace "MISTRAL_API_KEY=", ""

Write-Host "Clé Mistral détectée : $($MISTRAL_KEY.Substring(0,8))..." -ForegroundColor Yellow
Write-Host ""

# ── 1. Service Mistral ────────────────────────────────────────────
Write-Host "1. Création service mistral-llm..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services" -ContentType "application/json" -Body (@{
  name     = "mistral-llm"
  protocol = "https"
  host     = "api.mistral.ai"
  port     = 443
  path     = "/v1"
} | ConvertTo-Json)

# ── 2. Route /llm ─────────────────────────────────────────────────
Write-Host "2. Création route /llm..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mistral-llm/routes" -ContentType "application/json" -Body (@{
  name       = "llm-route"
  paths      = @("/llm")
  strip_path = $true
} | ConvertTo-Json)

# ── 3. Service MCP ────────────────────────────────────────────────
Write-Host "3. Création service mcp-server..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services" -ContentType "application/json" -Body (@{
  name     = "mcp-server"
  protocol = "http"
  host     = "mcp-server"
  port     = 3000
} | ConvertTo-Json)

# ── 3b. Service MCP Gemini ────────────────────────────────────────
Write-Host "3b. Création service mcp-server-gemini..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Method POST "$KONG/services" -ContentType "application/json" -ErrorAction Stop -Body (@{
        name     = "mcp-server-gemini"
        protocol = "http"
        host     = "mcp-server-gemini"
        port     = 3000
    } | ConvertTo-Json)
    Write-Host "   -> Service créé." -ForegroundColor Green
} catch {
    Write-Host "   -> Déjà existant ou erreur : $_" -ForegroundColor Yellow
}

# ── 4. Route /mcp ─────────────────────────────────────────────────
Write-Host "4. Création route /mcp..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mcp-server/routes" -ContentType "application/json" -Body (@{
  name       = "mcp-route"
  paths      = @("/mcp")
  strip_path = $true
} | ConvertTo-Json)

# ── 4b. Route /mcp-gemini ─────────────────────────────────────────
Write-Host "4b. Création route /mcp-gemini..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mcp-server-gemini/routes" -ContentType "application/json" -Body (@{
  name       = "mcp-gemini-route"
  # La route externe que LangGraph/n8n devra appeler sur Kong
  paths      = @("/mcp-gemini") 
  strip_path = $true
} | ConvertTo-Json)

# ── 5. Key Auth sur mistral-llm ───────────────────────────────────
Write-Host "5. Plugin Key Auth sur mistral-llm..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mistral-llm/plugins" -ContentType "application/json" -Body (@{
  name   = "key-auth"
  config = @{ key_names = @("apikey") }
} | ConvertTo-Json -Depth 5)

# ── 6. Key Auth sur mcp-server ────────────────────────────────────
Write-Host "6. Plugin Key Auth sur mcp-server..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mcp-server/plugins" -ContentType "application/json" -Body (@{
  name   = "key-auth"
  config = @{ key_names = @("apikey") }
} | ConvertTo-Json -Depth 5)

# ── 6b. Key Auth sur mcp-server-gemini ────────────────────────────
Write-Host "6b. Plugin Key Auth sur mcp-server-gemini..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mcp-server-gemini/plugins" -ContentType "application/json" -Body (@{
  name   = "key-auth"
  config = @{ key_names = @("apikey") }
} | ConvertTo-Json -Depth 5)

# ── 7. Request Transformer : injecter clé Mistral ─────────────────
Write-Host "7. Request Transformer (injection clé Mistral)..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/services/mistral-llm/plugins" -ContentType "application/json" -Body (@{
  name   = "request-transformer"
  config = @{
    replace = @{ headers = @("Authorization:Bearer $MISTRAL_KEY") }
    remove  = @{ headers = @("apikey") }
  }
} | ConvertTo-Json -Depth 5)

# ── 8. Consumer n8n-agent ─────────────────────────────────────────
Write-Host "8. Consumer n8n-agent..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/consumers" -ContentType "application/json" -Body (@{
  username = "n8n-agent"
} | ConvertTo-Json)

# ── 9. Clé interne pour n8n ───────────────────────────────────────
Write-Host "9. Clé interne n8n-internal-key-2025..." -ForegroundColor Cyan
Invoke-RestMethod -Method POST "$KONG/consumers/n8n-agent/key-auth" -ContentType "application/json" -Body (@{
  key = "n8n-internal-key-2025"
} | ConvertTo-Json)

Write-Host ""
Write-Host "Configuration Kong terminée !" -ForegroundColor Green