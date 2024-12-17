# Capturar MAC Address da interface ativa
$macAddressList = wmic nic where "NetConnectionStatus=2" get MACAddress /value | Select-String -Pattern "MACAddress="
$macAddress = $macAddressList | ForEach-Object { $_ -replace "MACAddress=", "" } | Select-Object -First 1

# Verificar se um MAC Address foi capturado
if (-not $macAddress) {
    Write-Error "Erro: Nenhum MAC Address foi capturado para interfaces de rede ativas."
    exit 1
}

Write-Host "MAC Address Capturado: $macAddress"

# Executar o comando wmic para obter a configuração do NIC com base no MAC Address
$nicConfigOutput = wmic nicconfig where "MACAddress='$macAddress'" get IPAddress /value

# Verificar se o comando wmic retornou algum resultado
if (-not $nicConfigOutput) {
    Write-Error "Erro: Não foi possível obter a configuração do NIC para o MAC Address $macAddress."
    exit 1
}

# Exibir o output para fins de depuração
Write-Host "Saida do NICConfig: $nicConfigOutput"

# Refinar para extrair a linha correta
$ipAddressLine = ($nicConfigOutput | Select-String -Pattern 'IPAddress' | Select-Object -First 1)

# Verificar se foi encontrada alguma linha com IPAddress
if (-not $ipAddressLine) {
    Write-Error "Erro: Nenhum endereço IP encontrado para o MAC Address $macAddress."
    exit 1
}

# Transformar a linha em string e remover formatação adicional (ex: { e })
$ipAddressLine = $ipAddressLine.ToString() -replace 'IPAddress=\{"?(.+?)"?\}', '$1'

# Se houver múltiplos endereços, pegar apenas o IPv4 e remover aspas adicionais
$ipAddress = $ipAddressLine -split "," | Where-Object { $_ -match '\d{1,3}(\.\d{1,3}){3}' } | Select-Object -First 1
$ipAddress = $ipAddress -replace '"', '' # Remover aspas duplas, se houver

# Verificação de erro após extração de IP
if (-not $ipAddress) {
    Write-Error "Erro: Nenhum endereço IP válido encontrado após processamento da saída."
    exit 1
}

# Caminho do arquivo .env
$envFilePath = Join-Path $PSScriptRoot ".env.production"

# Atualizar ou criar o arquivo .env com o IP
if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath
    $envContent = $envContent -replace '^HOST_IP=.*', "HOST_IP=$ipAddress"
    $envContent = $envContent -replace '^RUN_CONTAINER=.*', "RUN_CONTAINER=true"

    Set-Content -Path $envFilePath -Value $envContent
} else {
    Set-Content -Path $envFilePath -Value "HOST_IP=$ipAddress"
}
