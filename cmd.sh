curl -i http://localhost:3000/mcp -H "Authorization: Bearer <CLIENT_TOKEN>" -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-11-25\",\"capabilities\":{},\"clientInfo\":{\"name\":\"test\",\"version\":\"1.0\"}}}"

docker exec -it <container> python -c "import socket; s=socket.create_connection(('doris.toolkitdoris.ppe.euw.azure.tesco.org',9030),10); print('ok')"
