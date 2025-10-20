import React, { useState, useEffect, useMemo } from 'react';
import { Card, Row, Col, Statistic, Button, Space, Tag, Alert, Divider, Typography, message } from 'antd';
import { 
  ReloadOutlined, 
  BarChartOutlined, 
  LineChartOutlined,
  DownloadOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import jsPDF from 'jspdf';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area, BarChart, Bar
} from 'recharts';
import styled from 'styled-components';

const { Title, Text, Paragraph } = Typography;

const ResultsContainer = styled.div`
  .ant-card {
    margin-bottom: 16px;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  @keyframes drawLine {
    from {
      stroke-dasharray: 1000;
      stroke-dashoffset: 1000;
    }
    to {
      stroke-dasharray: 1000;
      stroke-dashoffset: 0;
    }
  }
  
  @keyframes glow {
    0%, 100% {
      filter: drop-shadow(0 0 5px rgba(24, 144, 255, 0.3));
    }
    50% {
      filter: drop-shadow(0 0 15px rgba(24, 144, 255, 0.6));
    }
  }
  
  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-10px);
    }
    60% {
      transform: translateY(-5px);
    }
  }
`;

const ChartContainer = styled.div`
  height: 400px;
  margin: 16px 0;
  animation: slideInUp 0.8s ease-out;
  
  &:hover {
    transform: translateY(-2px);
    transition: transform 0.3s ease;
  }
  
  .recharts-wrapper {
    animation: fadeIn 1s ease-in;
  }
  
  .recharts-line {
    animation: drawLine 2s ease-in-out;
  }
  
  .recharts-dot {
    animation: bounce 0.6s ease-in-out;
  }
`;

const MetricCard = styled(Card)`
  text-align: center;
  
  .ant-statistic-title {
    font-size: 14px;
    color: #666;
  }
  
  .ant-statistic-content {
    font-size: 24px;
    font-weight: bold;
  }
`;

const SimulationResults = ({ results, onReload }) => {
  // Supprimer les états qui causent des re-renders

  // Supprimer le useEffect qui cause le rechargement
  // Les données sont préparées directement dans le rendu

  const prepareChartData = () => {
    if (!results?.real_cumulative || !results?.simulated_provisions) return [];

    // Étendre les données pour correspondre à l'axe X : 0, 500, 1000, 1500, 2000
    const dataLength = results.real_cumulative.length;
    const specificPeriods = results?.x_axis_values || Array.from({length: dataLength}, (_, i) => Math.round((i / (dataLength - 1)) * 2000));

    // Données réelles avec la numérotation spécifique
    const realData = results.real_cumulative.map((value, index) => {
      const period = specificPeriods[index] || index + 1;
      return {
        period: period,
        value: value,
        type: 'Réel'
      };
    });

    // Utiliser les vraies trajectoires simulées du backend si disponibles
    if (results.simulated_cumulative && results.simulated_cumulative.length > 0) {
      let simulatedData = [];
      const maxSamples = Math.min(20, results.simulated_cumulative.length);
      
      for (let i = 0; i < maxSamples; i++) {
        const trajectory = results.simulated_cumulative[i];
        const sampleData = trajectory.map((value, index) => {
          const period = specificPeriods[index] || index + 1;
          return {
            period: period,
            value: value,
            type: `Simulation ${i + 1}`
          };
        });
        simulatedData.push(...sampleData);
      }
      
      return [...realData, ...simulatedData];
    }

    // Fallback: générer des données simulées basées sur les provisions (version stable)
    let simulatedData = [];
    const maxSamples = Math.min(20, results.simulated_provisions.length);
    
    for (let i = 0; i < maxSamples; i++) {
      const provision = results.simulated_provisions[i];
      const sampleData = [];
      const steps = Math.min(results.real_cumulative.length, specificPeriods.length);
      
      // Utiliser un seed basé sur l'index pour des valeurs stables
      const seed = i * 1000;
      
      for (let j = 0; j < steps; j++) {
        const period = specificPeriods[j] || j + 1;
        const realValue = results.real_cumulative[j] || 0;
        
        // Variation stable basée sur l'index et la provision
        const provisionRatio = provision / results.real_provision;
        const stableFactor = 0.5 + (Math.sin(seed + j) * 0.3); // Valeur stable entre 0.2 et 0.8
        const stableVariation = Math.sin(seed + j * 0.1) * (results.real_provision * 0.1);
        
        const simulatedValue = (realValue * provisionRatio * stableFactor) + stableVariation;
        
        sampleData.push({
          period: period,
          value: simulatedValue,
          type: `Simulation ${i + 1}`
        });
      }
      simulatedData.push(...sampleData);
    }

    return [...realData, ...simulatedData];
  };

  const prepareDensityData = () => {
    // Ne plus générer de courbe de densité côté frontend
    // La courbe est maintenant générée par le backend et affichée comme image
    return [];
  };

  const getRiskZone = (provision) => {
    if (!results.percentiles) return 'low';
    
    const { p95, p97_5, p99 } = results.percentiles;
    
    if (provision >= p99) return 'critical';
    if (provision >= p97_5) return 'high';
    if (provision >= p95) return 'medium';
    return 'low';
  };

  const getRiskZoneColor = (zone) => {
    const colors = {
      low: '#52c41a',
      medium: '#faad14',
      high: '#fa8c16',
      critical: '#f5222d'
    };
    return colors[zone] || '#d9d9d9';
  };

  const formatCurrency = (value) => {
    if (!value || isNaN(value)) return '0 FCFA';
    const numValue = Math.round(Number(value));
    return numValue.toLocaleString('fr-FR') + ' FCFA';
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Fonction d'export PDF
  const handleExport = () => {
    try {
      const doc = new jsPDF();
      let yPosition = 20;

      // Titre principal
      doc.setFontSize(20);
      doc.setFont('helvetica', 'bold');
      doc.text('Rapport de Simulation - EPSILON IA', 20, yPosition);
      yPosition += 15;

      // Informations de la simulation
      doc.setFontSize(12);
      doc.setFont('helvetica', 'normal');
      doc.text(`Méthode: ${results.method.toUpperCase()}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Échantillons: ${results.num_samples}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Niveau de confiance: ${formatPercentage(results.alpha)}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Date: ${new Date(results.created_at).toLocaleString()}`, 20, yPosition);
      yPosition += 20;

      // Informations clés des provisions
      doc.setFontSize(14);
      doc.setFont('helvetica', 'bold');
      doc.text('Informations Clés des Provisions', 20, yPosition);
      yPosition += 10;

      doc.setFontSize(12);
      doc.setFont('helvetica', 'normal');
      doc.text(`Provision Réelle: ${formatCurrency(results.real_provision)}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Provision 5% (P95): ${formatCurrency(results.percentiles?.['95%'] || 0)}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Provision 2.5% (P97.5): ${formatCurrency(results.percentiles?.['97.5%'] || 0)}`, 20, yPosition);
      yPosition += 8;
      doc.text(`Provision 1% (P99): ${formatCurrency(results.percentiles?.['99%'] || 0)}`, 20, yPosition);
      yPosition += 20;

      // Image de la trajectoire des transactions
      if (results.trajectory_plot?.image_base64) {
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.text('Trajectoire des Transactions', 20, yPosition);
        yPosition += 10;

        try {
          // Convertir l'image base64 en format utilisable
          const imgData = results.trajectory_plot.image_base64;
          const img = new Image();
          img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            
            const imgWidth = 160;
            const imgHeight = (img.height * imgWidth) / img.width;
            
            doc.addImage(imgData, 'PNG', 20, yPosition, imgWidth, imgHeight);
            yPosition += imgHeight + 20;

            // Image de la courbe de densité sur une nouvelle page
            if (results.density_curve?.image_base64) {
              // Nouvelle page pour la courbe de densité
              doc.addPage();
              yPosition = 20;
              
              doc.setFontSize(14);
              doc.setFont('helvetica', 'bold');
              doc.text('Courbe de Densité des Provisions', 20, yPosition);
              yPosition += 10;

              const densityImgData = results.density_curve.image_base64;
              const densityImg = new Image();
              densityImg.onload = function() {
                const densityCanvas = document.createElement('canvas');
                const densityCtx = densityCanvas.getContext('2d');
                densityCanvas.width = densityImg.width;
                densityCanvas.height = densityImg.height;
                densityCtx.drawImage(densityImg, 0, 0);
                
                // Image plus grande sur la deuxième page
                const densityImgWidth = 170;
                const densityImgHeight = (densityImg.height * densityImgWidth) / densityImg.width;
                
                doc.addImage(densityImgData, 'PNG', 15, yPosition, densityImgWidth, densityImgHeight);
                yPosition += densityImgHeight + 20;

                // Image des patterns temporels sur la même page ou nouvelle page
                if (results.patterns_plot?.image_base64) {
                  // Vérifier si on a assez d'espace sur la page actuelle
                  if (yPosition + 100 > 280) { // 280 est approximativement la hauteur d'une page A4
                    doc.addPage();
                    yPosition = 20;
                  }
                  
                  doc.setFontSize(14);
                  doc.setFont('helvetica', 'bold');
                  doc.text('Patterns Temporels - Emprunts et Remboursements', 20, yPosition);
                  yPosition += 10;

                  const patternsImgData = results.patterns_plot.image_base64;
                  const patternsImg = new Image();
                  patternsImg.onload = function() {
                    const patternsCanvas = document.createElement('canvas');
                    const patternsCtx = patternsCanvas.getContext('2d');
                    patternsCanvas.width = patternsImg.width;
                    patternsCanvas.height = patternsImg.height;
                    patternsCtx.drawImage(patternsImg, 0, 0);
                    
                    // Image des patterns (plus petite pour tenir sur la page)
                    const patternsImgWidth = 170;
                    const patternsImgHeight = (patternsImg.height * patternsImgWidth) / patternsImg.width;
                    
                    doc.addImage(patternsImgData, 'PNG', 15, yPosition, patternsImgWidth, patternsImgHeight);
                    
                    // Sauvegarder le PDF
                    doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
                    message.success('Rapport exporté avec succès !');
                  };
                  patternsImg.src = patternsImgData;
                } else {
                  // Sauvegarder le PDF même sans patterns
                  doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
                  message.success('Rapport exporté avec succès !');
                }
              };
              densityImg.src = densityImgData;
            } else {
              doc.addPage();
              doc.text('Image de densité non disponible', 20, 30);
              
              // Ajouter les patterns même si la densité n'est pas disponible
              if (results.patterns_plot?.image_base64) {
                doc.setFontSize(14);
                doc.setFont('helvetica', 'bold');
                doc.text('Patterns Temporels - Emprunts et Remboursements', 20, 50);
                
                const patternsImgData = results.patterns_plot.image_base64;
                const patternsImg = new Image();
                patternsImg.onload = function() {
                  const patternsCanvas = document.createElement('canvas');
                  const patternsCtx = patternsCanvas.getContext('2d');
                  patternsCanvas.width = patternsImg.width;
                  patternsCanvas.height = patternsImg.height;
                  patternsCtx.drawImage(patternsImg, 0, 0);
                  
                  const patternsImgWidth = 170;
                  const patternsImgHeight = (patternsImg.height * patternsImgWidth) / patternsImg.width;
                  
                  doc.addImage(patternsImgData, 'PNG', 15, 70, patternsImgWidth, patternsImgHeight);
                  
                  doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
                  message.success('Rapport exporté avec succès !');
                };
                patternsImg.src = patternsImgData;
              } else {
                doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
                message.success('Rapport exporté avec succès !');
              }
            }
          };
          img.src = imgData;
        } catch (error) {
          console.error('Erreur lors du traitement de l\'image:', error);
          doc.text('Erreur lors du chargement de l\'image de trajectoire', 20, yPosition);
          doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
          message.success('Rapport exporté avec succès !');
        }
      } else {
        doc.text('Images non disponibles', 20, yPosition);
        doc.save(`simulation_${results.method}_${new Date().toISOString().split('T')[0]}.pdf`);
        message.success('Rapport exporté avec succès !');
      }
    } catch (error) {
      console.error('Erreur lors de l\'export:', error);
      message.error('Erreur lors de l\'export du rapport');
    }
  };

  // Mémoriser les données pour éviter les re-renders causés par Math.random()
  const currentChartData = useMemo(() => {
    if (!results?.real_cumulative || !results?.simulated_provisions) return [];
    return prepareChartData();
  }, [results?.real_cumulative, results?.simulated_provisions, results?.real_provision, results?.x_axis_values]);
  
  const currentDensityData = useMemo(() => {
    return prepareDensityData();
  }, []);

  if (!results) {
    return (
      <Alert
        message="Aucun résultat disponible"
        description="Lancez une simulation pour voir les résultats"
        type="info"
        showIcon
      />
      );
  }

  return (
    <ResultsContainer>
      <Card 
        title={
          <Space>
            <BarChartOutlined />
            Résultats de la Simulation
            <Tag color="blue">{results.method.toUpperCase()}</Tag>
            <Tag color="green">{results.num_samples} échantillons</Tag>
          </Space>
        }
        extra={
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={onReload}
              type="primary"
            >
              Relancer
            </Button>
            <Button 
              icon={<DownloadOutlined />}
              onClick={handleExport}
            >
              Exporter
            </Button>
          </Space>
        }
      >
        {/* Métriques principales */}
        <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
          <Col span={6}>
            <MetricCard size="small">
              <Statistic
                title="Provision Réelle"
                value={formatCurrency(results.real_provision)}
                valueStyle={{ color: '#1890ff' }}
              />
            </MetricCard>
          </Col>
          <Col span={6}>
            <MetricCard size="small">
              <Statistic
                title="Moyenne Simulée"
                value={formatCurrency(
                  results.simulated_provisions.reduce((a, b) => a + b, 0) / 
                  results.simulated_provisions.length
                )}
                valueStyle={{ color: '#52c41a' }}
              />
            </MetricCard>
          </Col>
          <Col span={6}>
            <MetricCard size="small">
              <Statistic
                title="Niveau de Confiance"
                value={formatPercentage(results.alpha)}
                valueStyle={{ color: '#722ed1' }}
              />
            </MetricCard>
          </Col>
          <Col span={6}>
            <MetricCard size="small">
              <Statistic
                title="Échantillons"
                value={results.num_samples}
                valueStyle={{ color: '#fa8c16' }}
              />
            </MetricCard>
          </Col>
        </Row>

        {/* Graphique de trajectoire des transactions - Image Base64 intégrée */}
        <Card title="📈 Trajectoire des Transactions (Montants Cumulés)" size="small">
          <div style={{
            height: '500px',
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#fafafa',
            borderRadius: '8px',
            position: 'relative',
            overflow: 'hidden'
          }}>
            {results.trajectory_plot?.image_base64 ? (
              <img
                src={results.trajectory_plot.image_base64}
                alt={`Trajectoire des transactions ${results.method}`}
                style={{
                  maxWidth: '100%',
                  maxHeight: '100%',
                  objectFit: 'contain',
                  animation: 'fadeIn 0.5s ease-in',
                  borderRadius: '4px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
                }}
                onError={(e) => {
                  console.error('Erreur de chargement de l\'image:', e);
                  e.target.style.display = 'none';
                }}
              />
            ) : (
              <div style={{
                textAlign: 'center',
                color: '#666',
                animation: 'pulse 1.5s ease-in-out infinite'
              }}>
                <div style={{ fontSize: '24px', marginBottom: '16px' }}>📈</div>
                <div>Génération du graphique des trajectoires...</div>
                <div style={{ fontSize: '12px', marginTop: '8px' }}>
                  Cette opération peut prendre quelques secondes selon le nombre d'échantillons
                </div>
                <div style={{ fontSize: '10px', marginTop: '4px', color: '#999' }}>
                  Le backend génère l'image avec matplotlib et la convertit en base64
                </div>
              </div>
            )}
          </div>
        </Card>

            {/* Graphique de densité des provisions - Image Base64 intégrée */}
            <Card title={`📊 Courbe de Densité des Provisions (Méthode ${results.method})`} size="small">
              <div style={{
                height: '500px',
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: '#fafafa',
                borderRadius: '8px',
                position: 'relative',
                overflow: 'hidden'
              }}>
                {results.density_curve?.image_base64 ? (
                  <img
                    src={results.density_curve.image_base64}
                    alt={`Courbe de densité ${results.method}`}
                    style={{
                      maxWidth: '100%',
                      maxHeight: '100%',
                      objectFit: 'contain',
                      animation: 'fadeIn 0.5s ease-in',
                      borderRadius: '4px',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
                    }}
                    onError={(e) => {
                      console.error('Erreur de chargement de l\'image:', e);
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  <div style={{
                    textAlign: 'center',
                    color: '#666',
                    animation: 'pulse 1.5s ease-in-out infinite'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '16px' }}>📊</div>
                    <div>Génération de la courbe de densité...</div>
                    <div style={{ fontSize: '12px', marginTop: '8px' }}>
                      Cette opération peut prendre quelques secondes selon le nombre d'échantillons
                    </div>
                    <div style={{ fontSize: '10px', marginTop: '4px', color: '#999' }}>
                      Le backend génère l'image avec matplotlib et la convertit en base64
                    </div>
                  </div>
                )}
              </div>
          
          {/* Indicateurs de risque avec montants */}
                      <Row gutter={16} style={{ marginTop: 16 }}>
                        <Col span={8}>
                          <Card size="small" style={{ backgroundColor: '#90EE90', opacity: 0.8, border: '2px solid #90EE90' }}>
                            <Statistic 
                              title="Provision 5%" 
                              value={results.percentiles?.['95%'] || 0} 
                              formatter={(value) => formatCurrency(value)}
                              valueStyle={{ color: '#000', fontWeight: 'bold', fontSize: '16px' }}
                            />
                          </Card>
                        </Col>
                        <Col span={8}>
                          <Card size="small" style={{ backgroundColor: '#3CB371', opacity: 0.8, border: '2px solid #3CB371' }}>
                            <Statistic 
                              title="Provision 2.5%" 
                              value={results.percentiles?.['97.5%'] || 0} 
                              formatter={(value) => formatCurrency(value)}
                              valueStyle={{ color: '#000', fontWeight: 'bold', fontSize: '16px' }}
                            />
                          </Card>
                        </Col>
                        <Col span={8}>
                          <Card size="small" style={{ backgroundColor: '#006400', opacity: 0.8, border: '2px solid #006400' }}>
                            <Statistic 
                              title="Provision 1%" 
                              value={results.percentiles?.['99%'] || 0} 
                              formatter={(value) => formatCurrency(value)}
                              valueStyle={{ color: '#fff', fontWeight: 'bold', fontSize: '16px' }}
                            />
                          </Card>
                        </Col>
                      </Row>
        </Card>

        {/* Patterns Temporels */}
        <Card title={`📈 Patterns Temporels (Méthode ${results.method})`} size="small">
          <div style={{
            height: '500px',
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#fafafa',
            borderRadius: '8px',
            position: 'relative',
            overflow: 'hidden'
          }}>
            {results.patterns_plot?.image_base64 ? (
              <img
                src={results.patterns_plot.image_base64}
                alt={`Patterns temporels ${results.method}`}
                style={{
                  maxWidth: '100%',
                  maxHeight: '100%',
                  objectFit: 'contain',
                  animation: 'fadeIn 0.5s ease-in',
                  borderRadius: '4px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
                }}
                onError={(e) => {
                  console.error('Erreur de chargement de l\'image:', e);
                  e.target.style.display = 'none';
                }}
              />
            ) : (
              <div style={{
                textAlign: 'center',
                color: '#666',
                animation: 'pulse 1.5s ease-in-out infinite'
              }}>
                <div style={{ fontSize: '24px', marginBottom: '16px' }}>📈</div>
                <div>Génération des patterns temporels...</div>
                <div style={{ fontSize: '12px', marginTop: '8px' }}>
                  Cette opération peut prendre quelques secondes selon le nombre d'échantillons
                </div>
                <div style={{ fontSize: '10px', marginTop: '4px', color: '#999' }}>
                  Le backend génère l'image avec matplotlib et la convertit en base64
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Statistiques détaillées */}
        <Card title="📋 Statistiques Détaillées" size="small">
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Title level={5}>Percentiles</Title>
              <Row gutter={[8, 8]}>
                <Col span={8}>
                  <Text>P5: {formatCurrency(results.percentiles?.['5%'] || 0)}</Text>
                </Col>
                <Col span={8}>
                  <Text>P25: {formatCurrency(results.percentiles?.['25%'] || 0)}</Text>
                </Col>
                <Col span={8}>
                  <Text>P50: {formatCurrency(results.percentiles?.['50%'] || 0)}</Text>
                </Col>
                <Col span={8}>
                  <Text>P75: {formatCurrency(results.percentiles?.['75%'] || 0)}</Text>
                </Col>
                <Col span={8}>
                  <Text>P95: {formatCurrency(results.percentiles?.['95%'] || 0)}</Text>
                </Col>
                <Col span={8}>
                  <Text>P99: {formatCurrency(results.percentiles?.['99%'] || 0)}</Text>
                </Col>
              </Row>
            </Col>
            <Col span={12}>
              <Title level={5}>Intervalle de Confiance</Title>
              <Row gutter={[8, 8]}>
                <Col span={12}>
                  <Text>Niveau: {formatPercentage(results.alpha)}</Text>
                </Col>
                <Col span={12}>
                  <Text>Borne inférieure: {formatCurrency(results.confidence_interval?.lower || 0)}</Text>
                </Col>
                <Col span={12}>
                  <Text>Borne supérieure: {formatCurrency(results.confidence_interval?.upper || 0)}</Text>
                </Col>
              </Row>
            </Col>
          </Row>
        </Card>
      </Card>

      {/* Informations sur la simulation */}
      <Card title="ℹ️ Informations sur la Simulation" size="small">
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <Text strong>Méthode:</Text> {results.method}
          </Col>
          <Col span={8}>
            <Text strong>Statut:</Text> 
            <Tag color={results.status === 'completed' ? 'green' : 'orange'}>
              {results.status}
            </Tag>
          </Col>
          <Col span={8}>
            <Text strong>Créée le:</Text> {new Date(results.created_at).toLocaleString()}
          </Col>
          {results.completed_at && (
            <Col span={8}>
              <Text strong>Terminée le:</Text> {new Date(results.completed_at).toLocaleString()}
            </Col>
          )}
          <Col span={8}>
            <Text strong>Durée:</Text> {
              results.completed_at && results.created_at 
                ? `${Math.round((new Date(results.completed_at) - new Date(results.created_at)) / 1000)}s`
                : 'En cours...'
            }
          </Col>
        </Row>
      </Card>
    </ResultsContainer>
  );
};

export default SimulationResults;
