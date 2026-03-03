$ErrorActionPreference = "Stop"

$connectorName = "redis-sink-driver-location"
$connectorPath = ".\connectors\redis-sink-driver-location.json"
$connectorBody = Get-Content -Raw -Path $connectorPath
$connectorConfig = (Get-Content -Raw -Path $connectorPath | ConvertFrom-Json).config | ConvertTo-Json -Depth 10

try {
    Invoke-RestMethod -Method Post -Uri "http://localhost:8083/connectors" -ContentType "application/json" -Body $connectorBody | Out-Null
    Write-Host "Connector criado: $connectorName"
}
catch {
    $statusCode = $null
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
        $statusCode = [int]$_.Exception.Response.StatusCode
    }

    if ($statusCode -eq 409 -or $_.Exception.Message -match "already exists") {
        Invoke-RestMethod -Method Put -Uri "http://localhost:8083/connectors/$connectorName/config" -ContentType "application/json" -Body $connectorConfig | Out-Null
        Write-Host "Connector atualizado: $connectorName"
    }
    else {
        throw
    }
}

Invoke-RestMethod -Method Get -Uri "http://localhost:8083/connectors/$connectorName/status"
