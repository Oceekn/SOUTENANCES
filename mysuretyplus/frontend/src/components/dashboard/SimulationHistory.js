import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Tag, Typography, Modal, message, Tooltip, Popconfirm } from 'antd';
import { 
  ReloadOutlined, 
  DownloadOutlined, 
  EyeOutlined, 
  DeleteOutlined, 
  HistoryOutlined,
  FileExcelOutlined,
  FilePdfOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import styled from 'styled-components';
import axios from 'axios';
import { Row, Col } from 'antd'; // Added missing import for Row and Col

const { Title, Text } = Typography;

const HistoryContainer = styled.div`
  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .simulation-status {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .export-buttons {
    display: flex;
    gap: 8px;
  }
  
  .method-tag {
    font-weight: bold;
  }
  
  .results-preview {
    max-height: 300px;
    overflow-y: auto;
  }
`;

const SimulationHistory = () => {
  const [simulations, setSimulations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSimulation, setSelectedSimulation] = useState(null);
  const [previewModalVisible, setPreviewModalVisible] = useState(false);

  // Données simulées pour la démonstration
  const mockSimulations = [
    {
      id: 1,
      method: 'montecarlo',
      num_samples: 1000,
      alpha: 0.95,
      status: 'completed',
      created_at: '2024-01-15T10:30:00Z',
      completed_at: '2024-01-15T10:35:00Z',
      real_provision: 8500.50,
      simulated_provisions: [8200, 8300, 8400, 8500, 8600, 8700, 8800],
      percentiles: { '5%': 8200, '25%': 8300, '50%': 8500, '75%': 8700, '95%': 8800 },
      confidence_interval: { lower: 8200, upper: 8800 }
    },
    {
      id: 2,
      method: 'bootstrap',
      num_samples: 500,
      alpha: 0.99,
      status: 'completed',
      created_at: '2024-01-14T14:20:00Z',
      completed_at: '2024-01-14T14:28:00Z',
      real_provision: 8200.75,
      simulated_provisions: [8000, 8100, 8200, 8300, 8400],
      percentiles: { '1%': 8000, '5%': 8100, '50%': 8200, '95%': 8300, '99%': 8400 },
      confidence_interval: { lower: 8000, upper: 8400 }
    },
    {
      id: 3,
      method: 'montecarlo',
      num_samples: 2000,
      alpha: 0.90,
      status: 'running',
      created_at: '2024-01-15T11:00:00Z',
      completed_at: null,
      real_provision: null,
      simulated_provisions: [],
      percentiles: {},
      confidence_interval: {}
    }
  ];

  useEffect(() => {
    loadSimulations();
  }, []);

  const loadSimulations = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/simulations/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      setSimulations(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement de l\'historique:', error);
      message.error('Erreur lors du chargement de l\'historique');
      // Fallback sur les données mockées en cas d'erreur
      setSimulations(mockSimulations);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'running': return 'processing';
      case 'failed': return 'error';
      case 'pending': return 'warning';
      default: return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Terminé';
      case 'running': return 'En cours';
      case 'failed': return 'Échoué';
      case 'pending': return 'En attente';
      default: return 'Inconnu';
    }
  };

  const getMethodText = (method) => {
    switch (method) {
      case 'montecarlo': return 'Monte Carlo';
      case 'bootstrap': return 'Bootstrap';
      default: return method;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('fr-FR');
  };

  const handlePreview = (simulation) => {
    setSelectedSimulation(simulation);
    setPreviewModalVisible(true);
  };

  const handleReload = async (simulation) => {
    try {
      message.info('Relancement de la simulation...');
      const token = localStorage.getItem('token');
      await axios.post(`/api/simulations/${simulation.id}/reload/`, {}, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      message.success('Simulation relancée avec succès');
      loadSimulations();
    } catch (error) {
      console.error('Erreur lors du relancement:', error);
      message.error('Erreur lors du relancement');
    }
  };

  const handleDelete = async (simulationId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/simulations/${simulationId}/`, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      setSimulations(prev => prev.filter(s => s.id !== simulationId));
      message.success('Simulation supprimée');
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      message.error('Erreur lors de la suppression');
    }
  };

  const exportToCSV = (simulation) => {
    try {
      // Export CSV pour simulation
      message.info('Début de l\'export CSV...');
      
      if (!simulation) {
        message.error('Aucune simulation sélectionnée');
        return;
      }
      
      // Vérifier que la simulation a des données
      if (!simulation.id) {
        message.error('Données de simulation invalides');
        return;
      }
      
      // Créer le contenu CSV
      const csvContent = `Méthode,Échantillons,Alpha,Provision Réelle,Provision 5%,Provision 95%,IC Inférieur,IC Supérieur
${getMethodText(simulation.method)},${simulation.num_samples || 'N/A'},${simulation.alpha || 'N/A'},${simulation.real_provision || 'N/A'},${simulation.percentiles?.['5%'] || 'N/A'},${simulation.percentiles?.['95%'] || 'N/A'},${simulation.confidence_interval?.lower || 'N/A'},${simulation.confidence_interval?.upper || 'N/A'}`;
      
      // Contenu CSV généré
      
      // Créer et télécharger le fichier
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `simulation_${simulation.id}_${simulation.method || 'unknown'}.csv`;
      
      // Lien de téléchargement créé
      
      // Ajouter le lien au DOM, cliquer, puis le retirer
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Nettoyer l'URL après téléchargement
      setTimeout(() => URL.revokeObjectURL(url), 100);
      
      message.success('Export CSV réussi');
    } catch (error) {
      console.error('Erreur lors de l\'export CSV:', error);
      message.error('Erreur lors de l\'export CSV: ' + error.message);
    }
  };

  const exportToExcel = (simulation) => {
    try {
      // Export Excel pour simulation
      
      if (!simulation) {
        message.error('Aucune simulation sélectionnée');
        return;
      }
      
      // Vérifier que la simulation a des données
      if (!simulation.id) {
        message.error('Données de simulation invalides');
        return;
      }
      
      // Créer un fichier Excel simple avec les données de la simulation
      const data = [
        ['Méthode', 'Échantillons', 'Alpha', 'Provision Réelle', 'Provision 5%', 'Provision 95%', 'IC Inférieur', 'IC Supérieur'],
        [
          getMethodText(simulation.method),
          simulation.num_samples || 'N/A',
          simulation.alpha || 'N/A',
          simulation.real_provision || 'N/A',
          simulation.percentiles?.['5%'] || 'N/A',
          simulation.percentiles?.['95%'] || 'N/A',
          simulation.confidence_interval?.lower || 'N/A',
          simulation.confidence_interval?.upper || 'N/A'
        ]
      ];
      
      // Convertir en CSV pour l'instant (Excel peut ouvrir les CSV)
      const csvContent = data.map(row => row.join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `simulation_${simulation.id}_${simulation.method || 'unknown'}.xlsx`;
      
      // Ajouter le lien au DOM, cliquer, puis le retirer
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Nettoyer l'URL après téléchargement
      setTimeout(() => URL.revokeObjectURL(url), 100);
      
      message.success('Export Excel réussi');
    } catch (error) {
      console.error('Erreur lors de l\'export Excel:', error);
      message.error('Erreur lors de l\'export Excel: ' + error.message);
    }
  };

  const exportToPDF = (simulation) => {
    try {
      // Créer un rapport PDF simple
      const reportContent = `
RAPPORT DE SIMULATION
====================

ID: ${simulation.id}
Méthode: ${getMethodText(simulation.method)}
Échantillons: ${simulation.num_samples}
Alpha: ${simulation.alpha}
Statut: ${getStatusText(simulation.status)}
Créé le: ${formatDate(simulation.created_at)}

RÉSULTATS:
----------
Provision Réelle: ${simulation.real_provision || 'N/A'} €
Provision 5%: ${simulation.percentiles?.['5%'] || 'N/A'} €
Provision 95%: ${simulation.percentiles?.['95%'] || 'N/A'} €
Intervalle de Confiance: [${simulation.confidence_interval?.lower || 'N/A'}, ${simulation.confidence_interval?.upper || 'N/A'}]

Données Simulées: ${simulation.simulated_provisions?.length || 0} valeurs
      `;
      
      const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `rapport_simulation_${simulation.id}.txt`;
      link.click();
      
      message.success('Export PDF réussi (format texte)');
    } catch (error) {
      message.error('Erreur lors de l\'export PDF');
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Méthode',
      dataIndex: 'method',
      key: 'method',
      render: (method) => (
        <Tag color={method === 'montecarlo' ? 'blue' : 'purple'} className="method-tag">
          {getMethodText(method)}
        </Tag>
      ),
    },
    {
      title: 'Échantillons',
      dataIndex: 'num_samples',
      key: 'num_samples',
      width: 120,
    },
    {
      title: 'Alpha',
      dataIndex: 'alpha',
      key: 'alpha',
      width: 80,
      render: (alpha) => `${(alpha * 100).toFixed(0)}%`,
    },
    {
      title: 'Statut',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <div className="simulation-status">
          <Tag color={getStatusColor(status)}>
            {getStatusText(status)}
          </Tag>
        </div>
      ),
    },
    {
      title: 'Provision Réelle',
      dataIndex: 'real_provision',
      key: 'real_provision',
      width: 140,
      render: (value) => value ? `${value.toFixed(2)} €` : '-',
    },
    {
      title: 'Créé le',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (date) => formatDate(date),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 200,
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="Aperçu">
            <Button 
              type="text" 
              icon={<EyeOutlined />} 
              onClick={() => handlePreview(record)}
              size="small"
            />
          </Tooltip>
          
          {record.status === 'completed' && (
            <>
              <Tooltip title="Relancer">
                <Button 
                  type="text" 
                  icon={<ReloadOutlined />} 
                  onClick={() => handleReload(record)}
                  size="small"
                />
              </Tooltip>
              
              <Tooltip title="Exporter CSV">
                <Button 
                  type="text" 
                  icon={<FileTextOutlined />} 
                  onClick={() => exportToCSV(record)}
                  size="small"
                />
              </Tooltip>
            </>
          )}
          
          <Popconfirm
            title="Êtes-vous sûr de vouloir supprimer cette simulation ?"
            onConfirm={() => handleDelete(record.id)}
            okText="Oui"
            cancelText="Non"
          >
            <Tooltip title="Supprimer">
              <Button 
                type="text" 
                danger 
                icon={<DeleteOutlined />} 
                size="small"
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <HistoryContainer>
      <div className="history-header">
        <div>
          <Title level={3}>
            <HistoryOutlined /> Historique des Simulations
          </Title>
          <Text type="secondary">
            Gérez et analysez vos simulations précédentes
          </Text>
        </div>
        
        <div className="export-buttons">
          <Button 
            icon={<ReloadOutlined />} 
            onClick={loadSimulations}
            loading={loading}
          >
            Actualiser
          </Button>
          <Button 
            icon={<DownloadOutlined />} 
            onClick={() => {
              if (simulations.length > 0) {
                exportToCSV(simulations[0]);
              } else {
                message.warning('Aucune simulation à exporter');
              }
            }}
            type="primary"
          >
            Test Export
          </Button>
        </div>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={simulations}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => 
              `${range[0]}-${range[1]} sur ${total} simulations`,
          }}
          scroll={{ x: 1000 }}
        />
      </Card>

      {/* Modal d'aperçu des résultats */}
      <Modal
        title={`Aperçu - Simulation ${selectedSimulation?.id}`}
        open={previewModalVisible}
        onCancel={() => setPreviewModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setPreviewModalVisible(false)}>
            Fermer
          </Button>,
          selectedSimulation?.status === 'completed' && (
            <Button 
              key="export" 
              type="primary" 
              icon={<DownloadOutlined />}
              onClick={() => exportToCSV(selectedSimulation)}
            >
              Exporter CSV
            </Button>
          ),
        ].filter(Boolean)}
        width={800}
      >
        {selectedSimulation && (
          <div className="results-preview">
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <Card size="small" title="Paramètres">
                  <p><strong>Méthode:</strong> {getMethodText(selectedSimulation.method)}</p>
                  <p><strong>Échantillons:</strong> {selectedSimulation.num_samples}</p>
                  <p><strong>Alpha:</strong> {(selectedSimulation.alpha * 100).toFixed(0)}%</p>
                  <p><strong>Statut:</strong> {getStatusText(selectedSimulation.status)}</p>
                </Card>
              </Col>
              
              {selectedSimulation.status === 'completed' && (
                <Col span={12}>
                  <Card size="small" title="Résultats">
                    <p><strong>Provision Réelle:</strong> {selectedSimulation.real_provision?.toFixed(2)} €</p>
                    <p><strong>IC 95%:</strong> [{selectedSimulation.confidence_interval?.lower}, {selectedSimulation.confidence_interval?.upper}]</p>
                    <p><strong>Provision 5%:</strong> {selectedSimulation.percentiles?.['5%']} €</p>
                    <p><strong>Provision 95%:</strong> {selectedSimulation.percentiles?.['95%']} €</p>
                  </Card>
                </Col>
              )}
            </Row>
            
            {selectedSimulation.status === 'completed' && (
              <Card size="small" title="Données Simulées" style={{ marginTop: 16 }}>
                <Text type="secondary">
                  {selectedSimulation.simulated_provisions?.length || 0} valeurs simulées
                </Text>
                <div style={{ marginTop: 8 }}>
                  <Text code>
                    {selectedSimulation.simulated_provisions?.slice(0, 10).join(', ') || 'Aucune donnée'}
                    {selectedSimulation.simulated_provisions?.length > 10 && '...'}
                  </Text>
                </div>
              </Card>
            )}
          </div>
        )}
      </Modal>
    </HistoryContainer>
  );
};

export default SimulationHistory;

