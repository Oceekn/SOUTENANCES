import React, { useState } from 'react';
import { Card, Row, Col, Form, InputNumber, Button, Typography, Space, Divider, Alert, Statistic } from 'antd';
import { CalculatorOutlined, ArrowRightOutlined, InfoCircleOutlined } from '@ant-design/icons';
import axios from 'axios';
import styled from 'styled-components';

const { Title, Text, Paragraph } = Typography;

const CalculatorContainer = styled.div`
  .ant-card {
    margin-bottom: 16px;
  }
  
  .calculation-result {
    padding: 16px;
    border-radius: 8px;
    background: #f6ffed;
    border: 1px solid #b7eb8f;
    margin-top: 16px;
  }
`;

const RiskCalculator = ({ simulationResults }) => {
  // Props reçues pour le calcul de risque
  
  const [riskForm] = Form.useForm();
  const [provisionForm] = Form.useForm();
  const [riskResult, setRiskResult] = useState(null);
  const [provisionResult, setProvisionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateRiskForProvision = async (values) => {
    if (!simulationResults || !simulationResults.id) {
      console.error('Aucune simulation disponible');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`/api/simulations/${simulationResults.id}/calculate_risk/`, {
        calculation_type: 'provision_to_risk',
        target_provision: values.target_provision
      }, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      });

      setProvisionResult(response.data);
      setRiskResult(null);
    } catch (error) {
      console.error('Erreur lors du calcul du risque:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProvisionForRisk = async (values) => {
    if (!simulationResults || !simulationResults.id) {
      console.error('Aucune simulation disponible');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`/api/simulations/${simulationResults.id}/calculate_risk/`, {
        calculation_type: 'risk_to_provision',
        risk_level: values.risk_level
      }, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      });

      setRiskResult(response.data);
      setProvisionResult(null);
    } catch (error) {
      console.error('Erreur lors du calcul de la provision:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XAF',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const getRiskColor = (riskLevel) => {
    if (riskLevel >= 5) return '#cf1322'; // Rouge pour risque élevé (5%+)
    if (riskLevel >= 2) return '#fa8c16'; // Orange pour risque modéré (2-5%)
    if (riskLevel >= 1) return '#52c41a'; // Vert pour risque faible (1-2%)
    return '#52c41a'; // Vert pour risque très faible (<1%)
  };

  return (
    <CalculatorContainer>
      <Alert
        message="Calculateur de Risque Bidirectionnel"
        description="Calculez soit le niveau de risque pour une provision donnée, soit la provision nécessaire pour un niveau de risque spécifique."
        type="info"
        showIcon
        icon={<CalculatorOutlined />}
        style={{ marginBottom: 24 }}
      />

      <Row gutter={[24, 24]}>
        {/* Calcul du risque pour une provision donnée */}
        <Col xs={24} lg={12}>
          <Card title="🎯 Calcul du Niveau de Risque" size="small">
            <Paragraph>
              Saisissez une provision cible pour connaître le niveau de risque associé.
            </Paragraph>

            <Form
              form={provisionForm}
              layout="vertical"
              onFinish={calculateRiskForProvision}
            >
              <Form.Item
                name="target_provision"
                label="Provision Cible (XAF)"
                rules={[
                  { required: true, message: 'Veuillez saisir la provision cible' },
                  { type: 'number', min: 0, message: 'La provision doit être positive' }
                ]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  placeholder="Ex: 1000000"
                  formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value.replace(/\$\s?|(,*)/g, '')}
                  addonAfter="XAF"
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  icon={<CalculatorOutlined />}
                  block
                >
                  Calculer le Risque
                </Button>
              </Form.Item>
            </Form>

            {/* Résultat du calcul de risque */}
            {provisionResult && (
              <div className="calculation-result">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Text strong>Résultat du calcul :</Text>
                  <Text>
                    Pour une provision de <Text strong>{formatCurrency(provisionResult.target_provision)}</Text>,
                    le niveau de risque est de{' '}
                    <Text 
                      strong 
                      style={{ color: getRiskColor(provisionResult.risk_level) }}
                    >
                      {provisionResult.risk_level.toFixed(2)}%
                    </Text>
                  </Text>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Méthode utilisée : {provisionResult.method}
                  </Text>
                </Space>
              </div>
            )}
          </Card>
        </Col>

        {/* Calcul de la provision pour un niveau de risque donné */}
        <Col xs={24} lg={12}>
          <Card title="💰 Calcul de la Provision" size="small">
            <Paragraph>
              Saisissez un niveau de risque pour connaître la provision nécessaire.
            </Paragraph>

            <Form
              form={riskForm}
              layout="vertical"
              onFinish={calculateProvisionForRisk}
            >
              <Form.Item
                name="risk_level"
                label="Niveau de Risque (%)"
                rules={[
                  { required: true, message: 'Veuillez saisir le niveau de risque' },
                  { type: 'number', min: 0.1, max: 10, message: 'Le risque doit être entre 0.1% et 10%' }
                ]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  placeholder="Ex: 5"
                  min={0.1}
                  max={10}
                  step={0.1}
                  addonAfter="%"
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  icon={<CalculatorOutlined />}
                  block
                >
                  Calculer la Provision
                </Button>
              </Form.Item>
            </Form>

            {/* Résultat du calcul de provision */}
            {riskResult && (
              <div className="calculation-result">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Text strong>Résultat du calcul :</Text>
                  <Text>
                    Pour un risque de <Text strong style={{ color: getRiskColor(riskResult.risk_level) }}>
                      {riskResult.risk_level}%
                    </Text>,
                    la provision nécessaire est de{' '}
                    <Text strong style={{ color: '#1890ff' }}>
                      {formatCurrency(riskResult.provision_value)}
                    </Text>
                  </Text>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Méthode utilisée : {riskResult.method}
                  </Text>
                </Space>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      <Divider />

      {/* Informations sur l'interprétation des résultats */}
      <Card title="📚 Interprétation des Résultats" size="small">
        <Row gutter={[16, 16]}>
          <Col xs={24} md={8}>
            <Card size="small" style={{ borderLeft: '4px solid #52c41a' }}>
              <Statistic
                title="Risque Faible"
                value="1-2%"
                valueStyle={{ color: '#52c41a' }}
              />
              <Text type="secondary">Provision élevée, sécurité maximale</Text>
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small" style={{ borderLeft: '4px solid #faad14' }}>
              <Statistic
                title="Risque Modéré"
                value="2-5%"
                valueStyle={{ color: '#faad14' }}
              />
              <Text type="secondary">Équilibre risque/coût</Text>
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small" style={{ borderLeft: '4px solid #cf1322' }}>
              <Statistic
                title="Risque Élevé"
                value="5-10%"
                valueStyle={{ color: '#cf1322' }}
              />
              <Text type="secondary">Provision faible, risque élevé</Text>
            </Card>
          </Col>
        </Row>

        <Alert
          message="Note importante"
          description="Ces calculs sont basés sur les simulations effectuées. Plus le nombre d'échantillons est élevé, plus les résultats sont fiables."
          type="warning"
          showIcon
          icon={<InfoCircleOutlined />}
          style={{ marginTop: 16 }}
        />
      </Card>
    </CalculatorContainer>
  );
};

export default RiskCalculator;




