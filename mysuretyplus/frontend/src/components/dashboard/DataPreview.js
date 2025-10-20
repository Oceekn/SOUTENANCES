import React, { useState, useEffect, useCallback } from 'react';
import { Card, Table, Typography, Space, Tag, Alert, Button } from 'antd';
import { EyeOutlined, FileTextOutlined, InfoCircleOutlined } from '@ant-design/icons';
import styled from 'styled-components';

const { Text, Title } = Typography;

const PreviewContainer = styled.div`
  .ant-table {
    font-size: 12px;
  }
  
  .ant-table-thead > tr > th {
    padding: 8px;
    font-size: 11px;
  }
  
  .ant-table-tbody > tr > td {
    padding: 6px 8px;
  }
`;

const DataPreview = ({ lendingFile, recoveryFile }) => {
  const [lendingData, setLendingData] = useState([]);
  const [recoveryData, setRecoveryData] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [loading, setLoading] = useState(false);

  const loadDataPreview = useCallback(async () => {
    if (!lendingFile || !recoveryFile) return;
    
    setLoading(true);
    
    try {
      // Lire les vrais fichiers CSV uploadés
      const lendingText = await lendingFile.file.text();
      const recoveryText = await recoveryFile.file.text();
      
      // Parser les données CSV avec limitation pour éviter la surcharge
      const parseCSV = (csvText, maxRows = 20) => {
        const lines = csvText.trim().split('\n');
        const headers = lines[0].split(';');
        const data = [];
        
        // Limiter le nombre de lignes pour éviter la surcharge
        const maxLines = Math.min(lines.length, maxRows + 1);
        
        for (let i = 1; i < maxLines; i++) {
          const values = lines[i].split(';');
          const row = {};
          headers.forEach((header, index) => {
            row[header.trim()] = values[index] ? values[index].trim() : '';
          });
          data.push(row);
        }
        
        return data;
      };
      
      const lendingData = parseCSV(lendingText);
      const recoveryData = parseCSV(recoveryText);
      
      setLendingData(lendingData);
      setRecoveryData(recoveryData);
    } catch (error) {
      // En cas d'erreur, afficher un message d'erreur
      setLendingData([]);
      setRecoveryData([]);
    } finally {
      setLoading(false);
    }
  }, [lendingFile, recoveryFile]);

  useEffect(() => {
    if (lendingFile && recoveryFile && showPreview) {
      loadDataPreview();
    }
  }, [lendingFile, recoveryFile, showPreview, loadDataPreview]);

  const getLendingColumns = () => {
    if (!lendingData.length) return [];
    
    const baseColumns = [
      {
        title: 'Date',
        dataIndex: 'ref_date',
        key: 'ref_date',
        width: 100,
        fixed: 'left',
      },
      {
        title: 'Heure',
        dataIndex: 'INTERVAL',
        key: 'INTERVAL',
        width: 80,
        fixed: 'left',
      }
    ];

    // Colonnes dynamiques pour les montants
    const amountColumns = Object.keys(lendingData[0])
      .filter(key => key !== 'ref_date' && key !== 'INTERVAL')
      .map(key => ({
        title: `${key} XAF`,
        dataIndex: key,
        key: key,
        width: 80,
        align: 'center',
        render: (value) => (
          <Tag color={value > 0 ? 'blue' : 'default'}>
            {value}
          </Tag>
        )
      }));

    return [...baseColumns, ...amountColumns];
  };

  const getRecoveryColumns = () => {
    if (!recoveryData.length) return [];
    
    const baseColumns = [
      {
        title: 'Date',
        dataIndex: 'ref_date',
        key: 'ref_date',
        width: 100,
        fixed: 'left',
      },
      {
        title: 'Heure',
        dataIndex: 'INTERVAL',
        key: 'INTERVAL',
        width: 80,
        fixed: 'left',
      }
    ];

    // Colonnes dynamiques pour les montants
    const amountColumns = Object.keys(recoveryData[0])
      .filter(key => key !== 'ref_date' && key !== 'INTERVAL')
      .map(key => ({
        title: `${key} XAF`,
        dataIndex: key,
        key: key,
        width: 80,
        align: 'center',
        render: (value) => (
          <Tag color={value > 0 ? 'green' : 'default'}>
            {value}
          </Tag>
        )
      }));

    return [...baseColumns, ...amountColumns];
  };

  const calculateTotals = (data) => {
    if (!data.length) return {};
    
    const totals = {};
    const amountKeys = Object.keys(data[0]).filter(key => key !== 'ref_date' && key !== 'INTERVAL');
    
    amountKeys.forEach(key => {
      totals[key] = data.reduce((sum, row) => sum + (parseInt(row[key]) || 0), 0);
    });
    
    return totals;
  };

  const getLendingTotals = () => calculateTotals(lendingData);
  const getRecoveryTotals = () => calculateTotals(recoveryData);

  if (!lendingFile || !recoveryFile) {
    return null;
  }

  return (
    <Card 
      title={
        <Space>
          <FileTextOutlined />
          Aperçu des Données
        </Space>
      }
      size="small"
      style={{ marginTop: 16 }}
      extra={
        <Button
          type={showPreview ? 'default' : 'primary'}
          icon={<EyeOutlined />}
          onClick={() => setShowPreview(!showPreview)}
          size="small"
        >
          {showPreview ? 'Masquer' : 'Aperçu'}
        </Button>
      }
    >
      {showPreview && (
        <PreviewContainer>
          {loading && (
            <Alert
              message="Chargement en cours..."
              description="Lecture des fichiers CSV, veuillez patienter..."
              type="info"
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}
          
          <Alert
            message="Aperçu des données"
            description="Affichage des 20 premières lignes pour éviter la surcharge. Les colonnes numériques représentent le nombre de transactions par dénomination (50, 100, 200, 500, 1000, 2000, 5000 XAF)"
            type="info"
            showIcon
            icon={<InfoCircleOutlined />}
            style={{ marginBottom: 16 }}
          />

          {/* Aperçu des emprunts */}
          <div style={{ marginBottom: 24 }}>
            <Title level={5} style={{ color: '#1890ff', marginBottom: 8 }}>
              📈 Fichier Emprunts (Lending) - {lendingFile?.name}
            </Title>
            <Table
              columns={getLendingColumns()}
              dataSource={lendingData}
              size="small"
              pagination={false}
              scroll={{ x: 'max-content' }}
              loading={loading}
              rowKey={(record, index) => index}
            />
            
            {/* Totaux */}
            <div style={{ marginTop: 8, padding: '8px 12px', background: '#f0f8ff', borderRadius: 4 }}>
              <Text strong>Totaux: </Text>
              {Object.entries(getLendingTotals()).map(([key, value]) => (
                <Tag key={key} color="blue" style={{ margin: '2px 4px' }}>
                  {key}: {value}
                </Tag>
              ))}
            </div>
          </div>

          {/* Aperçu des remboursements */}
          <div style={{ marginBottom: 16 }}>
            <Title level={5} style={{ color: '#52c41a', marginBottom: 8 }}>
              📉 Fichier Remboursements (Recovery) - {recoveryFile?.name}
            </Title>
            <Table
              columns={getRecoveryColumns()}
              dataSource={recoveryData}
              size="small"
              pagination={false}
              scroll={{ x: 'max-content' }}
              loading={loading}
              rowKey={(record, index) => index}
            />
            
            {/* Totaux */}
            <div style={{ marginTop: 8, padding: '8px 12px', background: '#f6ffed', borderRadius: 4 }}>
              <Text strong>Totaux: </Text>
              {Object.entries(getRecoveryTotals()).map(([key, value]) => (
                <Tag key={key} color="green" style={{ margin: '2px 4px' }}>
                  {key}: {value}
                </Tag>
              ))}
            </div>
          </div>

          {/* Calcul de la provision */}
          <Alert
            message="Calcul de la Provision"
            description={
              <div>
                <Text>La provision est calculée comme suit :</Text>
                <ul style={{ margin: '8px 0', paddingLeft: 20 }}>
                  <li>Pour chaque ligne : somme = (50×n50) + (100×n100) + (200×n200) + ...</li>
                  <li>Différence = Emprunts - Remboursements</li>
                  <li>Solde cumulatif = somme des différences</li>
                  <li>Provision = maximum du solde cumulatif</li>
                </ul>
              </div>
            }
            type="success"
            showIcon
            style={{ marginTop: 16 }}
          />
        </PreviewContainer>
      )}
    </Card>
  );
};

export default DataPreview;





