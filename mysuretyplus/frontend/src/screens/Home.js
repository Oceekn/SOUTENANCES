import React, { useState, useEffect } from 'react';
import { Button, Typography, Space } from 'antd';
import { ArrowRightOutlined, InfoCircleOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import styled, { keyframes } from 'styled-components';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

// Animations
const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
`;

const typewriter = keyframes`
  0% {
    width: 0;
  }
  50% {
    width: 100%;
  }
  100% {
    width: 0;
  }
`;

const blink = keyframes`
  0%, 50% {
    border-color: transparent;
  }
  51%, 100% {
    border-color: #D4AF37;
  }
`;

const particleFloat = keyframes`
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(360deg);
    opacity: 0;
  }
`;

const glow = keyframes`
  0%, 100% {
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(212, 175, 55, 0.6), 0 0 60px rgba(212, 175, 55, 0.4);
  }
`;

const HomeContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #2D1B69 0%, #1E293B 50%, #2D1B69 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 20px;
`;

const Particle = styled.div`
  position: absolute;
  width: 4px;
  height: 4px;
  background: #D4AF37;
  border-radius: 50%;
  animation: ${particleFloat} ${props => props.duration || '8s'} linear infinite;
  left: ${props => props.left || '50%'};
  animation-delay: ${props => props.delay || '0s'};
  box-shadow: 0 0 10px #D4AF37;
`;

const LogoContainer = styled.div`
  text-align: center;
  margin-bottom: 60px;
  animation: ${fadeInUp} 1.5s ease-out;
  position: relative;
  z-index: 10;
`;

const LogoCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 40px 60px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  animation: ${glow} 3s ease-in-out infinite;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: shimmer 3s infinite;
  }
  
  @keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
  }
`;

const LogoImage = styled.img`
  width: 300px;
  height: auto;
  margin-bottom: 20px;
  animation: ${pulse} 2s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  
  @media (max-width: 768px) {
    width: 250px;
  }
`;


const PoweredByContainer = styled.div`
  text-align: center;
  margin-bottom: 40px;
  animation: ${fadeInUp} 1.5s ease-out 0.5s both;
`;

const PoweredByText = styled.div`
  font-size: 48px;
  font-weight: bold;
  color: #D4AF37;
  text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
  overflow: hidden;
  white-space: nowrap;
  border-right: 4px solid #D4AF37;
  animation: ${typewriter} 4s steps(20, end) infinite, ${blink} 0.75s step-end infinite;
  margin: 0 auto;
  max-width: fit-content;
  
  @media (max-width: 768px) {
    font-size: 32px;
  }
`;

const Slogan = styled.div`
  font-size: 24px;
  color: rgba(255, 255, 255, 0.9);
  font-style: italic;
  margin-top: 20px;
  animation: ${fadeInUp} 1.5s ease-out 1s both;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  
  @media (max-width: 768px) {
    font-size: 18px;
  }
`;

const ActionButtons = styled.div`
  margin-top: 40px;
  animation: ${fadeInUp} 1.5s ease-out 1.5s both;
`;

const StyledButton = styled(Button)`
  height: 60px;
  padding: 0 40px;
  font-size: 18px;
  border-radius: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  transition: all 0.4s ease;
  margin: 15px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
  border: none;
  color: #1E293B;
  font-weight: bold;
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(212, 175, 55, 0.4);
    background: linear-gradient(135deg, #E6C547 0%, #D4AF37 100%);
  }
  
  &:active {
    transform: translateY(-2px) scale(1.02);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.5s;
  }
  
  &:hover::before {
    left: 100%;
  }
`;

const SecondaryButton = styled(Button)`
  height: 50px;
  padding: 0 30px;
  font-size: 16px;
  border-radius: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
  }
`;

const Home = () => {
  const navigate = useNavigate();
  const [audioPlayed, setAudioPlayed] = useState(false);

  // Audio de bienvenue automatique
  useEffect(() => {
    if (!audioPlayed) {
      const timer = setTimeout(() => {
        const utterance = new SpeechSynthesisUtterance("Bienvenu à EPSILON IA, prêt à commencer ?");
        utterance.lang = 'fr-FR';
        utterance.rate = 0.8;
        utterance.pitch = 1.1;
        utterance.volume = 0.8;
        
        // Utiliser une voix de femme si disponible
        const voices = speechSynthesis.getVoices();
        const femaleVoice = voices.find(voice => 
          voice.lang.includes('fr') && 
          (voice.name.includes('female') || voice.name.includes('woman') || voice.name.includes('femme'))
        );
        
        if (femaleVoice) {
          utterance.voice = femaleVoice;
        }
        
        speechSynthesis.speak(utterance);
        setAudioPlayed(true);
      }, 2000); // Délai de 2 secondes après le chargement

      return () => clearTimeout(timer);
    }
  }, [audioPlayed]);

  // Générer des particules
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    duration: 8 + Math.random() * 4,
    delay: Math.random() * 8,
  }));

  return (
    <HomeContainer>
      {/* Particules flottantes */}
      {particles.map(particle => (
        <Particle
          key={particle.id}
          left={`${particle.left}%`}
          duration={`${particle.duration}s`}
          delay={`${particle.delay}s`}
        />
      ))}

      <LogoContainer>
        <LogoCard>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <LogoImage 
              src="/images/epsilon-ai-logo.jpg" 
              alt="EPSILON IA Logo"
            />
          </div>
        </LogoCard>
      </LogoContainer>

      <PoweredByContainer>
        <PoweredByText>POWERED BY EPSILON IA</PoweredByText>
        <Slogan>Look beyond what you see</Slogan>
      </PoweredByContainer>

      <ActionButtons>
        <Space size="large" wrap style={{ width: '100%', justifyContent: 'center' }}>
            <StyledButton
              type="primary"
              size="large"
              icon={<ArrowRightOutlined />}
              onClick={() => navigate('/login')}
              style={{ minWidth: '220px' }}
            >
              Se Connecter
            </StyledButton>
            
            <SecondaryButton
              size="large"
              icon={<InfoCircleOutlined />}
              onClick={() => navigate('/about')}
              style={{ minWidth: '160px' }}
            >
              À Propos
            </SecondaryButton>
            
            <SecondaryButton
              size="large"
              icon={<QuestionCircleOutlined />}
              onClick={() => navigate('/faq')}
              style={{ minWidth: '160px' }}
            >
              FAQ
            </SecondaryButton>
        </Space>
      </ActionButtons>
    </HomeContainer>
  );
};

export default Home;