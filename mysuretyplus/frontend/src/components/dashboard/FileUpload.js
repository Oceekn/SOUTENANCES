import React, { useState, useCallback } from 'react';
import { Upload, Card, Alert, Button, Space, Typography, Row, Col } from 'antd';
import { InboxOutlined, FileTextOutlined, BarChartOutlined } from '@ant-design/icons';
import styled from 'styled-components';

const { Dragger } = Upload;
const { Title, Text } = Typography;

const StyledCard = styled(Card)`
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 768px) {
    margin-bottom: 12px;
  }
`;

const FormatInfo = styled.div`
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
  
  @media (max-width: 768px) {
    padding: 12px;
    margin-bottom: 12px;
  }
  
  code {
    @media (max-width: 768px) {
      font-size: 11px;
      word-break: break-all;
    }
  }
`;

const FileSection = styled.div`
  text-align: center;
  padding: 24px;
  
  @media (max-width: 768px) {
    padding: 16px;
  }
`;

const UploadIcon = styled.div`
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 16px;
  
  @media (max-width: 768px) {
    font-size: 36px;
    margin-bottom: 12px;
  }
`;

const ResponsiveContainer = styled.div`
  @media (max-width: 768px) {
    .ant-typography {
      font-size: 14px !important;
    }
    
    .ant-upload-drag {
      padding: 16px 8px !important;
    }
    
    .ant-upload-drag p {
      font-size: 13px !important;
      margin-bottom: 8px !important;
    }
  }
`;

const FileUpload = ({ onFilesUploaded }) => {
  const [lendingFile, setLendingFile] = useState(null);
  const [recoveryFile, setRecoveryFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState({});

  const handleFileUpload = useCallback(async (file, fileType) => {
    try {
      const content = await readCSVFile(file);
      const isValid = validateCSVStructure(content, fileType);
      
      if (isValid) {
        setUploadStatus(prev => ({
          ...prev,
          [fileType]: { status: 'success', message: 'Fichier valide' }
        }));
        
        const fileObject = { file, content };
        
        if (fileType === 'lending') {
          setLendingFile(fileObject);
        } else {
          setRecoveryFile(fileObject);
        }
        
        // Notifier le parent si les deux fichiers sont prêts
        if ((fileType === 'lending' && recoveryFile) || (fileType === 'recovery' && lendingFile)) {
          onFilesUploaded({
            lending: fileType === 'lending' ? fileObject : lendingFile,
            recovery: fileType === 'recovery' ? fileObject : recoveryFile
          });
        }
      } else {
        setUploadStatus(prev => ({
          ...prev,
          [fileType]: { status: 'error', message: 'Format de fichier invalide' }
        }));
      }
    } catch (error) {
      setUploadStatus(prev => ({
        ...prev,
        [fileType]: { status: 'error', message: 'Erreur lors de la lecture du fichier' }
      }));
    }
  }, [lendingFile, recoveryFile, onFilesUploaded]);

  const readCSVFile = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsText(file);
    });
  };

  const validateCSVStructure = (content, fileType) => {
    const lines = content.split('\n');
    if (lines.length < 2) return false;
    
    const headers = lines[0].split(';').map(h => h.trim());
    
    if (fileType === 'lending') {
      // Colonnes exactes pour lending: ref_date, interval, 50, 100, 200, 250, 500, 1000, 1500, 2000, 2500, 5000
      const requiredColumns = ['ref_date', 'INTERVAL', '50', '100', '200', '250', '500', '1000', '1500', '2000', '2500', '5000'];
      return requiredColumns.every(col => headers.includes(col));
    } else if (fileType === 'recovery') {
      // Colonnes exactes pour recovery: SDATE, INTERVAL, 5, 34, 50, 61, 90, 100, 125, 173, 200, 215, 235, 250, 300, 435, 500, 600, 870, 1000, 1080, 1350, 1500, 1624, 1917, 2000, 2096, 2390, 2500, 3000, 4001, 5000
      const requiredColumns = ['SDATE', 'INTERVAL', '5', '34', '50', '61', '90', '100', '125', '173', '200', '215', '235', '250', '300', '435', '500', '600', '870', '1000', '1080', '1350', '1500', '1624', '1917', '2000', '2096', '2390', '2500', '3000', '4001', '5000'];
      return requiredColumns.every(col => headers.includes(col));
    }
    
    return false;
  };

  const removeFile = (fileType) => {
    if (fileType === 'lending') {
      setLendingFile(null);
    } else {
      setRecoveryFile(null);
    }
    setUploadStatus(prev => ({
      ...prev,
      [fileType]: null
    }));
  };

  const lendingUploadProps = {
    name: 'lending',
    multiple: false,
    accept: '.csv',
    beforeUpload: (file) => {
      handleFileUpload(file, 'lending');
      return false; // Empêcher l'upload automatique
    },
    showUploadList: false
  };

  const recoveryUploadProps = {
    name: 'recovery',
    multiple: false,
    accept: '.csv',
    beforeUpload: (file) => {
      handleFileUpload(file, 'recovery');
      return false; // Empêcher l'upload automatique
    },
    showUploadList: false
  };



  return (
    <ResponsiveContainer>
      <StyledCard>
        <Title level={3}>
          <FileTextOutlined /> Upload des Fichiers CSV
        </Title>


        <Row gutter={[16, 16]}>
          {/* Fichier des Emprunts */}
          <Col xs={24} sm={24} md={12} lg={12} xl={12}>
            <StyledCard>
              <FileSection>
                <Title level={4}>
                  <FileTextOutlined /> <BarChartOutlined /> Fichier des Emprunts (Lending)
                </Title>
                
                {lendingFile ? (
                  <div>
                    <UploadIcon>📄</UploadIcon>
                    <p><strong>{lendingFile.file.name}</strong></p>
                    <Space>
                      <Button type="primary" onClick={() => removeFile('lending')}>
                        Remplacer
                      </Button>
                    </Space>
                  </div>
                ) : (
                  <Dragger {...lendingUploadProps}>
                    <UploadIcon>
                      <InboxOutlined />
                    </UploadIcon>
                    <p>Cliquez ou glissez le fichier CSV des emprunts</p>
                  </Dragger>
                )}
                
                {uploadStatus.lending && (
                  <Alert
                    message={uploadStatus.lending.message}
                    type={uploadStatus.lending.status}
                    showIcon
                    style={{ marginTop: 16 }}
                  />
                )}
              </FileSection>
            </StyledCard>
          </Col>

          {/* Fichier des Remboursements */}
          <Col xs={24} sm={24} md={12} lg={12} xl={12}>
            <StyledCard>
              <FileSection>
                <Title level={4}>
                  <FileTextOutlined /> <BarChartOutlined /> Fichier des Remboursements (Recovery)
                </Title>
                
                {recoveryFile ? (
                  <div>
                    <UploadIcon>📄</UploadIcon>
                    <p><strong>{recoveryFile.file.name}</strong></p>
                    <Space>
                      <Button type="primary" onClick={() => removeFile('recovery')}>
                        Remplacer
                      </Button>
                    </Space>
                  </div>
                ) : (
                  <Dragger {...recoveryUploadProps}>
                    <UploadIcon>
                      <InboxOutlined />
                    </UploadIcon>
                    <p>Cliquez ou glissez le fichier CSV des remboursements</p>
                  </Dragger>
                )}
                
                {uploadStatus.recovery && (
                  <Alert
                    message={uploadStatus.recovery.message}
                    type={uploadStatus.recovery.status}
                    showIcon
                    style={{ marginTop: 16 }}
                  />
                )}
              </FileSection>
            </StyledCard>
          </Col>
        </Row>
      </StyledCard>
    </ResponsiveContainer>
  );
};

export default FileUpload;
