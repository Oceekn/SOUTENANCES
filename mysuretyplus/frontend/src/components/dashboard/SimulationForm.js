import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Form, InputNumber, Radio, Button, Card, message, Progress, Alert, Space, Tag } from 'antd';
import { PlayCircleOutlined, ReloadOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import axios from 'axios';

const SimulationFormContainer = styled.div`
  margin-bottom: 24px;
`;

const FileStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px 12px;
  background: #f6f8fa;
  border-radius: 6px;
  border-left: 4px solid #1890ff;
`;

const SimulationForm = ({ lendingFile, recoveryFile, onSimulationStarted }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [currentSimulation, setCurrentSimulation] = useState(null);
  const [simulationStatus, setSimulationStatus] = useState(null);
  const [progress, setProgress] = useState(0);
  const onSimulationStartedRef = useRef(onSimulationStarted);
  const monitoringRef = useRef(null);

  // Configuration par défaut
  const defaultValues = {
    method: 'montecarlo',
    num_samples: 1000,
    alpha: 0.95
  };

  useEffect(() => {
    form.setFieldsValue(defaultValues);
  }, [form]);

  // Mettre à jour la référence du callback
  useEffect(() => {
    onSimulationStartedRef.current = onSimulationStarted;
  }, [onSimulationStarted]);

  // Nettoyage du monitoring lors du démontage du composant
  useEffect(() => {
    return () => {
      // Nettoyer les timeouts et arrêter le monitoring
      if (monitoringRef.current && typeof monitoringRef.current === 'function') {
        monitoringRef.current();
        monitoringRef.current = null;
      }
      // Nettoyage du composant
    };
  }, []);

  // Vérifier si les fichiers sont prêts
  const filesReady = lendingFile && recoveryFile;

  const handleSubmit = async (values) => {
    if (!filesReady) {
      message.error('Veuillez d\'abord uploader les deux fichiers CSV');
      return;
    }

    try {
      setLoading(true);
      setProgress(0);

      // Créer un FormData pour l'upload des fichiers
      const formData = new FormData();
      formData.append('method', values.method);
      formData.append('num_samples', values.num_samples);
      formData.append('alpha', values.alpha);
      
      // Ajouter les fichiers correctement
      formData.append('lending_file', lendingFile.file);
      formData.append('recovery_file', recoveryFile.file);

      // Lancer la simulation
      const response = await axios.post('/api/simulations/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      });

      const simulation = response.data;
      
      if (!simulation || !simulation.id) {
        message.error('Erreur: Simulation non créée correctement');
        return;
      }
      
      setCurrentSimulation(simulation);
      setSimulationStatus('pending');
      
      message.success('Simulation lancée avec succès !');
      
      // Notifier le parent
      if (onSimulationStartedRef.current) {
        onSimulationStartedRef.current(simulation);
      }

      // Commencer le monitoring du statut
      const stopMonitoring = monitorSimulationStatus(simulation.id);
      monitoringRef.current = stopMonitoring;

    } catch (error) {
      if (error.response?.data?.error) {
        message.error(`Erreur: ${error.response.data.error}`);
      } else if (error.response?.status === 401) {
        message.error('Session expirée. Veuillez vous reconnecter.');
      } else {
        message.error('Erreur lors du lancement de la simulation');
      }
    } finally {
      setLoading(false);
    }
  };

  const monitorSimulationStatus = useCallback(async (simulationId) => {
    let isMonitoring = true; // Flag pour arrêter le monitoring
    
    const checkStatus = async () => {
      if (!isMonitoring) return; // Arrêter si le flag est false
      
      try {
        const response = await axios.get(`/api/simulations/${simulationId}/status/`, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });

        const status = response.data.status;
        setSimulationStatus(status);

        if (status === 'running') {
          // Progression stable sans Math.random()
          setProgress(prev => {
            const increment = 5; // Incrément fixe
            return Math.min(prev + increment, 90);
          });
          if (isMonitoring) {
            setTimeout(checkStatus, 3000); // Augmenter l'intervalle à 3 secondes
          }
        } else if (status === 'completed') {
          isMonitoring = false; // Arrêter le monitoring
          setProgress(100);
          message.success('Simulation terminée avec succès !');
          // Notifier le parent que la simulation est terminée
          if (onSimulationStartedRef.current) {
            onSimulationStartedRef.current({ ...currentSimulation, status: 'completed' });
          }
        } else if (status === 'failed') {
          isMonitoring = false; // Arrêter le monitoring
          message.error('La simulation a échoué');
          setProgress(0);
        }
      } catch (error) {
        if (isMonitoring) {
          setTimeout(checkStatus, 5000); // Réessayer dans 5 secondes
        }
      }
    };

    checkStatus();
    
    // Retourner une fonction pour arrêter le monitoring
    return () => {
      isMonitoring = false;
    };
  }, [currentSimulation]);

  const getStatusDisplay = () => {
    if (!currentSimulation) return null;

    const statusConfig = {
      pending: {
        icon: <ClockCircleOutlined />,
        color: '#faad14',
        text: 'En attente',
        description: 'La simulation est en file d\'attente'
      },
      running: {
        icon: <ClockCircleOutlined />,
        color: '#1890ff',
        text: 'En cours',
        description: 'Calcul en cours...'
      },
      completed: {
        icon: <CheckCircleOutlined />,
        color: '#52c41a',
        text: 'Terminé',
        description: 'Simulation terminée avec succès'
      },
      failed: {
        icon: <ReloadOutlined />,
        color: '#ff4d4f',
        text: 'Échoué',
        description: 'La simulation a échoué'
      }
    };

    const config = statusConfig[simulationStatus] || statusConfig.pending;

    return (
      <Alert
        message={
          <Space>
            {config.icon}
            <span>Statut: {config.text}</span>
          </Space>
        }
        description={config.description}
        type={simulationStatus === 'completed' ? 'success' : simulationStatus === 'failed' ? 'error' : 'info'}
        showIcon={false}
        style={{ marginBottom: '16px' }}
      />
    );
  };

  const getProgressDisplay = () => {
    if (!currentSimulation || !['pending', 'running'].includes(simulationStatus)) {
      return null;
    }

    return (
      <div style={{ marginBottom: '16px' }}>
        <Progress 
          percent={Math.round(progress)} 
          status={simulationStatus === 'running' ? 'active' : 'normal'}
          strokeColor={{
            '0%': '#108ee9',
            '100%': '#87d068',
          }}
        />
        <div style={{ textAlign: 'center', marginTop: '8px', color: '#666' }}>
          {simulationStatus === 'pending' ? 'En attente...' : 'Calcul en cours...'}
        </div>
      </div>
    );
  };

  return (
    <SimulationFormContainer>
      <Card title="Configuration de la Simulation" size="small">
        {/* Statut des fichiers */}
        <FileStatus>
          <Tag color={filesReady ? 'green' : 'orange'}>
            {filesReady ? '✓' : '⚠'}
          </Tag>
          <span>
            {filesReady 
              ? 'Fichiers prêts pour la simulation'
              : 'Veuillez uploader les fichiers CSV'
            }
          </span>
        </FileStatus>

        {/* Formulaire de configuration */}
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={defaultValues}
        >
          <Form.Item
            name="method"
            label="Méthodes Computationnelles"
            rules={[{ required: true, message: 'Veuillez sélectionner une méthode' }]}
          >
            <Radio.Group>
              <Radio.Button value="montecarlo">
                <Space>
                  🎲 Monte Carlo
                  <Tag color="blue">Simulation</Tag>
                </Space>
              </Radio.Button>
              <Radio.Button value="bootstrap">
                <Space>
                  🔄 Bootstrap
                  <Tag color="green">Rééchantillonnage</Tag>
                </Space>
              </Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item
            name="num_samples"
            label="Nombre d'Échantillons"
            rules={[
              { required: true, message: 'Veuillez spécifier le nombre d\'échantillons' },
              { type: 'number', min: 10, message: 'Minimum 10 échantillons' },
              { type: 'number', max: 15000, message: 'Maximum 15,000 échantillons' }
            ]}
          >
            <InputNumber
              min={10}
              max={15000}
              style={{ width: '100%' }}
              placeholder="Ex: 1000"
              addonAfter="échantillons"
            />
          </Form.Item>

          <Form.Item
            name="alpha"
            label="Niveau de Confiance (α)"
            rules={[
              { required: true, message: 'Veuillez spécifier le niveau de confiance' },
              { type: 'number', min: 0.5, message: 'Minimum 0.5' },
              { type: 'number', max: 0.999, message: 'Maximum 0.999' }
            ]}
          >
            <InputNumber
              min={0.5}
              max={0.999}
              step={0.001}
              style={{ width: '100%' }}
              placeholder="Ex: 0.95"
              addonAfter="(95% = 0.95)"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              disabled={!filesReady}
              icon={<PlayCircleOutlined />}
              size="large"
              style={{ width: '100%' }}
            >
              {loading ? 'Lancement...' : 'Lancer la Simulation'}
            </Button>
          </Form.Item>
        </Form>

        {/* Affichage du statut et de la progression */}
        {currentSimulation && (
          <>
            {getStatusDisplay()}
            {getProgressDisplay()}
          </>
        )}

        {/* Informations sur les méthodes */}
        <div style={{ marginTop: '16px', padding: '12px', background: '#f6f8fa', borderRadius: '6px' }}>
          <h5>📚 Méthodes de Simulation :</h5>
          <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
            <li><strong>Monte Carlo :</strong> Génération aléatoire basée sur la distribution de Poisson des données historiques</li>
            <li><strong>Bootstrap :</strong> Rééchantillonnage avec remise des données historiques existantes</li>
            <li><strong>Échantillons :</strong> Plus le nombre est élevé, plus les résultats sont précis (mais plus long à calculer)</li>
            <li><strong>Niveau de confiance :</strong> Détermine la précision de l'intervalle de confiance des résultats</li>
          </ul>
        </div>
      </Card>
    </SimulationFormContainer>
  );
};

export default SimulationForm;
