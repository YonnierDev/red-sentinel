def analyze_threat(network_data: dict) -> dict:
    """
    Función principal para analizar amenazas de red
    
    Args:
        network_data: Diccionario con datos de la red a analizar
        
    Returns:
        dict: Resultado del análisis con nivel de riesgo y recomendaciones
    """
    # Aquí irá la lógica del modelo de ML
    # Por ahora, devolvemos un ejemplo estático
    return {
        "risk_level": "MEDIUM",
        "threat_type": "Port Scanning",
        "confidence": 0.85,
        "recommendations": [
            "Bloquear IP de origen temporalmente",
            "Monitorear actividad sospechosa",
            "Revisar logs de red"
        ],
        "affected_ports": network_data.get("ports", []),
        "source_ip": network_data.get("source_ip", "unknown")
    }