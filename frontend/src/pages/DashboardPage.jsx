import { useState, useEffect } from 'react';
import { Brain, Upload, FileText, ChevronRight, Briefcase, BookOpen, ExternalLink } from 'lucide-react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { resumeAPI, rolesAPI } from '../services/api';

// Add CSS animations
const styles = `
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  .fade-in {
    animation: fadeIn 0.3s ease-out;
  }

  .slide-in {
    animation: slideIn 0.4s ease-out;
  }
`;

const DashboardPage = () => {
  // Inject styles
  useEffect(() => {
    const styleTag = document.createElement('style');
    styleTag.innerHTML = styles;
    document.head.appendChild(styleTag);
    return () => {
      document.head.removeChild(styleTag);
    };
  }, []);
  const [loading, setLoading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  // Collapsible sections state
  const [expandedSections, setExpandedSections] = useState({
    summary: false,
    workHistory: false,
    skills: true,
    education: false
  });

  // Selected role for detailed view
  const [selectedRole, setSelectedRole] = useState(null);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [coursesData, setCoursesData] = useState([]);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    console.log('Uploading file:', file.name, file.type, file.size);

    // Validate file
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'text/plain'
    ];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!validTypes.includes(file.type)) {
      setUploadError(`Invalid file type: ${file.type}. Please upload PDF, DOCX, or TXT files.`);
      return;
    }

    if (file.size > maxSize) {
      setUploadError('File size exceeds 5MB limit.');
      return;
    }

    setUploadError(null);
    setLoading(true);

    try {
      console.log('Calling upload API...');
      const uploadResponse = await resumeAPI.upload(file);
      console.log('Upload response:', uploadResponse);

      if (uploadResponse.resume_id) {
        console.log('Fetching parsed data for ID:', uploadResponse.resume_id);
        // Fetch parsed resume data
        const resumeResponse = await resumeAPI.getParsed(uploadResponse.resume_id);
        console.log('Parsed resume data:', resumeResponse);
        setResumeData(resumeResponse);

        // Fetch recommendations
        console.log('Fetching recommendations...');
        const recData = await rolesAPI.getRecommendations(uploadResponse.resume_id, 5);
        console.log('Recommendations:', recData);
        setRecommendations(recData);
      }
    } catch (error) {
      console.error('Upload error:', error);
      console.error('Error response:', error.response);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to upload resume. Please try again.';
      setUploadError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Handle role selection
  const handleRoleClick = async (role) => {
    setSelectedRole(role);

    // Fetch courses for weak and missing skills
    setLoadingCourses(true);
    try {
      const skillsToImprove = [
        ...role.skill_match_details.weak_skills.map(s => s.skill),
        ...role.skill_match_details.missing_skills.map(s => s.skill)
      ].slice(0, 5); // Get top 5 skills that need improvement

      // Simulated course fetch - in production, call a real API
      const courses = await fetchCoursesForSkills(skillsToImprove);
      setCoursesData(courses);
    } catch (error) {
      console.error('Error fetching courses:', error);
      setCoursesData([]);
    } finally {
      setLoadingCourses(false);
    }
  };

  // Fetch course recommendations for specific skills
  const fetchCoursesForSkills = async (skills) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Comprehensive course recommendations with real URLs
    const coursesMap = {
      // DevOps & Cloud
      'Kubernetes': {
        title: 'Kubernetes for Beginners',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/learn-kubernetes/'
      },
      'Docker': {
        title: 'Docker Mastery: Complete Toolset',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/docker-mastery/'
      },
      'Terraform': {
        title: 'Terraform for AWS - Beginner to Advanced',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/terraform-beginner-to-advanced/'
      },
      'AWS': {
        title: 'AWS Certified Solutions Architect Associate',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/'
      },
      'Jenkins': {
        title: 'Learn DevOps: CI/CD with Jenkins',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/learn-devops-ci-cd-with-jenkins-using-pipelines-and-docker/'
      },
      'Ansible': {
        title: 'Ansible for Beginners',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/learn-ansible/'
      },
      'Linux': {
        title: 'Linux Administration Bootcamp',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/linux-administration-bootcamp/'
      },
      'Monitoring': {
        title: 'Prometheus and Grafana Monitoring',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/prometheus-and-grafana/'
      },
      'CI/CD': {
        title: 'DevOps: CI/CD with Jenkins Pipelines',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/learn-devops-ci-cd-with-jenkins-using-pipelines-and-docker/'
      },

      // Programming Languages
      'Python': {
        title: 'Complete Python Bootcamp',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/complete-python-bootcamp/'
      },
      'JavaScript': {
        title: 'The Complete JavaScript Course',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/the-complete-javascript-course/'
      },
      'Java': {
        title: 'Java Programming Masterclass',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/java-the-complete-java-developer-course/'
      },
      'Go': {
        title: 'Learn Go Programming - Golang',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/learn-go-the-complete-bootcamp-course-golang/'
      },

      // Machine Learning & AI
      'Machine Learning': {
        title: 'Machine Learning A-Z',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/machinelearning/'
      },
      'Deep Learning': {
        title: 'Deep Learning Specialization',
        provider: 'Coursera',
        level: 'Advanced',
        url: 'https://www.coursera.org/specializations/deep-learning'
      },
      'TensorFlow': {
        title: 'TensorFlow Developer Certificate',
        provider: 'Coursera',
        level: 'Intermediate',
        url: 'https://www.coursera.org/professional-certificates/tensorflow-in-practice'
      },
      'PyTorch': {
        title: 'PyTorch for Deep Learning',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/pytorch-for-deep-learning-with-python-bootcamp/'
      },

      // Databases
      'SQL': {
        title: 'The Complete SQL Bootcamp',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/the-complete-sql-bootcamp/'
      },
      'MongoDB': {
        title: 'MongoDB - The Complete Guide',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/mongodb-the-complete-developers-guide/'
      },
      'PostgreSQL': {
        title: 'Complete PostgreSQL Database Course',
        provider: 'Udemy',
        level: 'Beginner',
        url: 'https://www.udemy.com/course/the-complete-python-postgresql-developer-course/'
      },

      // Web Development
      'React': {
        title: 'React - The Complete Guide',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/'
      },
      'Node.js': {
        title: 'Node.js - The Complete Guide',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/nodejs-the-complete-guide/'
      },
      'Angular': {
        title: 'Angular - The Complete Guide',
        provider: 'Udemy',
        level: 'Intermediate',
        url: 'https://www.udemy.com/course/the-complete-guide-to-angular-2/'
      }
    };

    return skills.map(skill =>
      coursesMap[skill] || {
        title: `${skill} Complete Course`,
        provider: 'Udemy',
        level: 'Beginner',
        url: `https://www.udemy.com/courses/search/?q=${encodeURIComponent(skill)}`
      }
    );
  };

  // Prepare radar chart data - show top candidate skills
  const getRadarChartData = () => {
    if (!resumeData?.extracted_data?.skills?.technical) return [];

    // Get top 8 skills by proficiency score
    const technicalSkills = resumeData.extracted_data.skills.technical
      .filter(skill => typeof skill === 'object' && skill.proficiency_score)
      .sort((a, b) => b.proficiency_score - a.proficiency_score)
      .slice(0, 8);

    return technicalSkills.map(skill => ({
      skill: skill.name,
      value: skill.proficiency_score,
      fullMark: 5
    }));
  };

  // Mock course recommendations
  const courseRecommendations = [
    {
      title: 'Deep Learning Specialization',
      level: 'Beginner',
      provider: 'Coursera',
      tag: 'Adsense Ad App'
    },
    {
      title: 'AWS Certified Solutions Architect',
      level: 'Advanced',
      provider: 'Udacity',
      tag: 'Adsense Ad App'
    }
  ];

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 50%, #e3f2fd 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Brain style={{ width: '64px', height: '64px', color: '#14b8a6', margin: '0 auto 16px' }} className="animate-pulse" />
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>
            Analyzing Your Resume...
          </h2>
          <p style={{ color: '#6b7280' }}>This will take just a few seconds</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 50%, #e3f2fd 100%)',
    }}>
      {/* Header */}
      <header style={{
        background: 'white',
        borderBottom: '1px solid #e5e7eb',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
        backdropFilter: 'blur(8px)',
        backgroundColor: 'rgba(255, 255, 255, 0.9)'
      }}>
        <div style={{
          maxWidth: '1536px',
          margin: '0 auto',
          padding: '16px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Brain style={{ width: '32px', height: '32px', color: '#14b8a6' }} />
            <h1 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              background: 'linear-gradient(135deg, #14b8a6 0%, #06b6d4 50%, #3b82f6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              margin: 0
            }}>
              Intelligent Career Platform
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div style={{ padding: '24px' }}>
        {/* Hero Section - Only show when no resume is uploaded */}
        {!resumeData && (
          <div style={{
            textAlign: 'center',
            maxWidth: '800px',
            margin: '0 auto 48px',
            padding: '24px'
          }}>
            <h2 style={{
              fontSize: '40px',
              fontWeight: 'bold',
              color: '#1f2937',
              marginBottom: '16px',
              lineHeight: '1.2'
            }}>
              Upload your resume and get instant job role recommendations powered by machine learning
            </h2>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '16px',
              fontSize: '14px',
              color: '#14b8a6',
              fontWeight: '500',
              marginBottom: '48px'
            }}>
              <span>No account needed</span>
              <span>•</span>
              <span>Instant results</span>
              <span>•</span>
              <span>100% free</span>
            </div>

            {/* Feature Highlights */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '24px',
              marginTop: '48px'
            }}>
              <div style={{
                padding: '24px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                textAlign: 'center'
              }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  background: 'linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px'
                }}>
                  <Brain style={{ width: '24px', height: '24px', color: 'white' }} />
                </div>
                <h3 style={{
                  fontSize: '18px',
                  fontWeight: 'bold',
                  color: '#1f2937',
                  marginBottom: '8px'
                }}>
                  AI-Powered Analysis
                </h3>
                <p style={{
                  fontSize: '14px',
                  color: '#6b7280',
                  lineHeight: '1.6'
                }}>
                  Advanced NLP and ML algorithms analyze your skills and experience
                </p>
              </div>

              <div style={{
                padding: '24px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                textAlign: 'center'
              }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  background: 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px'
                }}>
                  <Briefcase style={{ width: '24px', height: '24px', color: 'white' }} />
                </div>
                <h3 style={{
                  fontSize: '18px',
                  fontWeight: 'bold',
                  color: '#1f2937',
                  marginBottom: '8px'
                }}>
                  Smart Matching
                </h3>
                <p style={{
                  fontSize: '14px',
                  color: '#6b7280',
                  lineHeight: '1.6'
                }}>
                  Get matched with job roles that align with your unique skill set
                </p>
              </div>

              <div style={{
                padding: '24px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                textAlign: 'center'
              }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px'
                }}>
                  <ChevronRight style={{ width: '24px', height: '24px', color: 'white' }} />
                </div>
                <h3 style={{
                  fontSize: '18px',
                  fontWeight: 'bold',
                  color: '#1f2937',
                  marginBottom: '8px'
                }}>
                  Skill Gap Analysis
                </h3>
                <p style={{
                  fontSize: '14px',
                  color: '#6b7280',
                  lineHeight: '1.6'
                }}>
                  Identify skill gaps and get personalized recommendations
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Top Section - Two Columns */}
        <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '24px',
        marginBottom: '24px'
      }}>
        {/* Left: Upload Resume Card */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          padding: '32px'
        }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '400px'
          }}>
            <div style={{
              width: '96px',
              height: '96px',
              background: '#ccfbf1',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '24px'
            }}>
              <FileText style={{ width: '48px', height: '48px', color: '#14b8a6' }} />
            </div>

            <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>
              Upload Your Resume
            </h2>
            <p style={{ color: '#6b7280', marginBottom: '32px' }}>or drag and drop files here</p>

            {/* Drag and Drop Area */}
            <div
              style={{
                width: '100%',
                maxWidth: '448px',
                border: `2px dashed ${dragActive ? '#14b8a6' : '#d1d5db'}`,
                borderRadius: '12px',
                padding: '48px',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'border-color 0.2s',
                background: dragActive ? '#f0fdfa' : 'transparent'
              }}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf,.docx,.doc,.txt"
                style={{ display: 'none' }}
                id="resume-upload"
                onChange={handleFileInput}
              />
              <label htmlFor="resume-upload" style={{ cursor: 'pointer' }}>
                <Upload style={{ width: '48px', height: '48px', color: '#9ca3af', margin: '0 auto 12px', display: 'block' }} />
                <p style={{ color: '#4b5563', fontWeight: '500' }}>Click to browse</p>
                <p style={{ fontSize: '14px', color: '#9ca3af', marginTop: '4px' }}>PDF, DOCX, TXT (max 5MB)</p>
              </label>
            </div>

            {uploadError && (
              <div style={{
                marginTop: '16px',
                width: '100%',
                maxWidth: '448px',
                background: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                padding: '12px'
              }}>
                <p style={{ color: '#dc2626', fontSize: '14px' }}>{uploadError}</p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Parsed Skills & Experience */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          padding: '24px'
        }}>
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', marginBottom: '24px' }}>
            Parsed Skills & Experience
          </h2>

          {!resumeData ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: '#6b7280' }}>
              <FileText style={{ width: '48px', height: '48px', margin: '0 auto 16px', opacity: 0.3 }} />
              <p>Upload a resume to see parsed data</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {/* Summary Section */}
              <div style={{
                border: `1px solid ${expandedSections.summary ? '#5eead4' : '#e5e7eb'}`,
                background: expandedSections.summary ? '#f0fdfa' : 'white',
                borderRadius: '8px',
                transition: 'all 0.2s'
              }}>
                <button
                  onClick={() => toggleSection('summary')}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '16px',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    borderRadius: '8px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      background: expandedSections.summary ? '#14b8a6' : '#9ca3af'
                    }} />
                    <span style={{ fontWeight: '500', color: '#374151' }}>Summary</span>
                  </div>
                  <ChevronRight style={{
                    width: '20px',
                    height: '20px',
                    color: '#9ca3af',
                    transform: expandedSections.summary ? 'rotate(90deg)' : 'rotate(0deg)',
                    transition: 'transform 0.2s'
                  }} />
                </button>
                {expandedSections.summary && resumeData?.extracted_data?.summary && (
                  <div style={{ padding: '0 16px 16px 16px' }}>
                    <p style={{ fontSize: '14px', color: '#4b5563' }}>{resumeData.extracted_data.summary}</p>
                  </div>
                )}
              </div>

              {/* Work History Section */}
              <div style={{
                border: `1px solid ${expandedSections.workHistory ? '#5eead4' : '#e5e7eb'}`,
                background: expandedSections.workHistory ? '#f0fdfa' : 'white',
                borderRadius: '8px',
                transition: 'all 0.2s'
              }}>
                <button
                  onClick={() => toggleSection('workHistory')}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '16px',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    borderRadius: '8px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      background: expandedSections.workHistory ? '#14b8a6' : '#9ca3af'
                    }} />
                    <span style={{ fontWeight: '500', color: '#374151' }}>
                      Work History ({resumeData?.extracted_data?.experience?.length || 0} Jobs)
                    </span>
                  </div>
                  <ChevronRight style={{
                    width: '20px',
                    height: '20px',
                    color: '#9ca3af',
                    transform: expandedSections.workHistory ? 'rotate(90deg)' : 'rotate(0deg)',
                    transition: 'transform 0.2s'
                  }} />
                </button>
                {expandedSections.workHistory && resumeData?.extracted_data?.experience && (
                  <div style={{ padding: '0 16px 16px 16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {resumeData.extracted_data.experience.map((exp, idx) => (
                      <div key={idx} style={{ borderLeft: '2px solid #14b8a6', paddingLeft: '12px' }}>
                        <p style={{ fontWeight: '500', color: '#1f2937' }}>{exp.title || exp.role}</p>
                        <p style={{ fontSize: '14px', color: '#4b5563' }}>{exp.company}</p>
                        <p style={{ fontSize: '12px', color: '#6b7280' }}>{exp.duration || exp.period}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Skills Section */}
              <div style={{
                border: `1px solid ${expandedSections.skills ? '#5eead4' : '#e5e7eb'}`,
                background: expandedSections.skills ? '#f0fdfa' : 'white',
                borderRadius: '8px',
                transition: 'all 0.2s'
              }}>
                <button
                  onClick={() => toggleSection('skills')}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '16px',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    borderRadius: '8px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      background: expandedSections.skills ? '#14b8a6' : '#9ca3af'
                    }} />
                    <span style={{ fontWeight: '500', color: '#374151' }}>Skills</span>
                  </div>
                  <span style={{
                    background: '#14b8a6',
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '9999px',
                    fontSize: '14px',
                    fontWeight: '500'
                  }}>
                    Skills
                  </span>
                </button>
                {expandedSections.skills && (
                  <div style={{ padding: '0 16px 16px 16px' }}>
                    <div style={{ marginBottom: '12px' }}>
                      <p style={{ fontSize: '12px', fontWeight: '600', color: '#6b7280', marginBottom: '8px' }}>
                        TECHNICAL SKILLS
                      </p>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                        {resumeData?.extracted_data?.skills?.technical?.map((skill, idx) => {
                          const skillName = typeof skill === 'string' ? skill : skill.name;
                          const proficiency = typeof skill === 'object' ? skill.proficiency_score : null;
                          return (
                            <span
                              key={idx}
                              style={{
                                padding: '4px 12px',
                                background: '#ccfbf1',
                                color: '#0f766e',
                                borderRadius: '9999px',
                                fontSize: '14px'
                              }}
                            >
                              {skillName}
                              {proficiency && <span style={{ marginLeft: '4px', color: '#14b8a6' }}>({proficiency})</span>}
                            </span>
                          );
                        })}
                      </div>
                    </div>
                    {resumeData?.extracted_data?.skills?.soft && (
                      <div>
                        <p style={{ fontSize: '12px', fontWeight: '600', color: '#6b7280', marginBottom: '8px' }}>
                          SOFT SKILLS
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                          {resumeData.extracted_data.skills.soft.map((skill, idx) => {
                            const skillName = typeof skill === 'string' ? skill : skill.name;
                            return (
                              <span
                                key={idx}
                                style={{
                                  padding: '4px 12px',
                                  background: '#f3e8ff',
                                  color: '#6b21a8',
                                  borderRadius: '9999px',
                                  fontSize: '14px'
                                }}
                              >
                                {skillName}
                              </span>
                            );
                          })}
                        </div>
                      </div>
                    )}
                    <p style={{ fontSize: '12px', color: '#6b7280', marginTop: '12px' }}>
                      Skills ({resumeData?.extracted_data?.skills?.technical?.length || 0}+)
                    </p>
                  </div>
                )}
              </div>

              {/* Education Section */}
              <div style={{
                border: `1px solid ${expandedSections.education ? '#5eead4' : '#e5e7eb'}`,
                background: expandedSections.education ? '#f0fdfa' : 'white',
                borderRadius: '8px',
                transition: 'all 0.2s'
              }}>
                <button
                  onClick={() => toggleSection('education')}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '16px',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    borderRadius: '8px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      background: expandedSections.education ? '#14b8a6' : '#9ca3af'
                    }} />
                    <span style={{ fontWeight: '500', color: '#374151' }}>Education</span>
                  </div>
                  <ChevronRight style={{
                    width: '20px',
                    height: '20px',
                    color: '#9ca3af',
                    transform: expandedSections.education ? 'rotate(90deg)' : 'rotate(0deg)',
                    transition: 'transform 0.2s'
                  }} />
                </button>
                {expandedSections.education && resumeData?.extracted_data?.education && (
                  <div style={{ padding: '0 16px 16px 16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {resumeData.extracted_data.education.map((edu, idx) => (
                      <div key={idx} style={{ borderLeft: '2px solid #a855f7', paddingLeft: '12px' }}>
                        <p style={{ fontWeight: '500', color: '#1f2937' }}>{edu.degree}</p>
                        <p style={{ fontSize: '14px', color: '#4b5563' }}>{edu.institution}</p>
                        <p style={{ fontSize: '12px', color: '#6b7280' }}>{edu.year || edu.period}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Section - Three Columns */}
      {resumeData && recommendations && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '24px'
        }}>
          {/* Left: Suggested Roles */}
          <div style={{
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            padding: '24px'
          }}>
            <h3 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
              Suggested Roles
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {recommendations?.recommendations?.slice(0, 5).map((rec, idx) => (
                <div
                  key={idx}
                  onClick={() => handleRoleClick(rec)}
                  style={{
                    border: `2px solid ${selectedRole?.role?.title === rec.role.title ? '#14b8a6' : '#e5e7eb'}`,
                    borderRadius: '8px',
                    padding: '16px',
                    transition: 'all 0.2s',
                    cursor: 'pointer',
                    background: selectedRole?.role?.title === rec.role.title ? '#f0fdfa' : 'white'
                  }}
                  onMouseEnter={(e) => {
                    if (selectedRole?.role?.title !== rec.role.title) {
                      e.currentTarget.style.borderColor = '#14b8a6';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedRole?.role?.title !== rec.role.title) {
                      e.currentTarget.style.borderColor = '#e5e7eb';
                    }
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '12px' }}>
                    <div style={{
                      width: '40px',
                      height: '40px',
                      background: '#dbeafe',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <Briefcase style={{ width: '20px', height: '20px', color: '#2563eb' }} />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <h4 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '4px' }}>{rec.role.title}</h4>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                        <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#14b8a6' }}>
                          {Math.round(rec.suitability_percentage)}%
                        </span>
                        <span style={{ fontSize: '14px', color: '#6b7280' }}>Match</span>
                      </div>
                    </div>
                  </div>

                  <p style={{ fontSize: '14px', color: '#4b5563', marginBottom: '12px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {rec.match_explanation}
                  </p>

                  <div style={{ display: 'flex', gap: '8px', fontSize: '12px' }}>
                    <span style={{ padding: '4px 8px', background: '#dcfce7', color: '#166534', borderRadius: '4px' }}>
                      {rec.skill_match_details.matched_skills.length} matched
                    </span>
                    <span style={{ padding: '4px 8px', background: '#fef3c7', color: '#854d0e', borderRadius: '4px' }}>
                      {rec.skill_match_details.weak_skills.length} weak
                    </span>
                    <span style={{ padding: '4px 8px', background: '#fee2e2', color: '#991b1b', borderRadius: '4px' }}>
                      {rec.skill_match_details.missing_skills.length} missing
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Center: Skill Gap Details or Visualization */}
          <div style={{
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            padding: '24px'
          }}>
            {!selectedRole ? (
              <>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
                  Skill Gap Visualization
                </h3>

                <div style={{ height: '350px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={getRadarChartData()}>
                      <PolarGrid stroke="#d1d5db" />
                      <PolarAngleAxis
                        dataKey="skill"
                        tick={{ fill: '#6b7280', fontSize: 12 }}
                      />
                      <PolarRadiusAxis
                        angle={90}
                        domain={[0, 5]}
                        tick={{ fill: '#9ca3af', fontSize: 10 }}
                      />
                      <Radar
                        name="Your Skills"
                        dataKey="value"
                        stroke="#14b8a6"
                        fill="#14b8a6"
                        fillOpacity={0.5}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>

                <div style={{ marginTop: '16px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px', color: '#4b5563' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#14b8a6' }} />
                    <span>Current Level</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#d1d5db' }} />
                    <span>Target Level</span>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937' }}>
                    Skill Gap Analysis
                  </h3>
                  <button
                    onClick={() => setSelectedRole(null)}
                    style={{
                      padding: '6px 12px',
                      fontSize: '12px',
                      color: '#6b7280',
                      background: '#f3f4f6',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer'
                    }}
                  >
                    Clear
                  </button>
                </div>

                <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '16px' }}>
                  Skills you need to improve for <strong>{selectedRole.role.title}</strong>
                </p>

                {/* Skill Gaps with Progress Bars */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {/* Matched Skills */}
                  {selectedRole.skill_match_details.matched_skills.length > 0 && (
                    <div>
                      <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#166534', marginBottom: '8px' }}>
                        ✓ Strong Skills ({selectedRole.skill_match_details.matched_skills.length})
                      </h4>
                      {selectedRole.skill_match_details.matched_skills.slice(0, 3).map((skill, idx) => (
                        <div key={idx} style={{ marginBottom: '8px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                            <span style={{ fontWeight: '500', color: '#1f2937' }}>{skill.skill}</span>
                            <span style={{ color: '#6b7280' }}>{skill.user_level}/{skill.required_level}</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', background: '#e5e7eb', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{
                              width: `${(skill.user_level / skill.required_level) * 100}%`,
                              height: '100%',
                              background: '#10b981',
                              borderRadius: '3px'
                            }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Weak Skills */}
                  {selectedRole.skill_match_details.weak_skills.length > 0 && (
                    <div>
                      <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#854d0e', marginBottom: '8px' }}>
                        ⚠ Skills to Strengthen ({selectedRole.skill_match_details.weak_skills.length})
                      </h4>
                      {selectedRole.skill_match_details.weak_skills.slice(0, 3).map((skill, idx) => (
                        <div key={idx} style={{ marginBottom: '8px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                            <span style={{ fontWeight: '500', color: '#1f2937' }}>{skill.skill}</span>
                            <span style={{ color: '#6b7280' }}>{skill.user_level}/{skill.required_level}</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', background: '#e5e7eb', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{
                              width: `${(skill.user_level / skill.required_level) * 100}%`,
                              height: '100%',
                              background: '#f59e0b',
                              borderRadius: '3px'
                            }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Missing Skills */}
                  {selectedRole.skill_match_details.missing_skills.length > 0 && (
                    <div>
                      <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#991b1b', marginBottom: '8px' }}>
                        ✕ Skills to Learn ({selectedRole.skill_match_details.missing_skills.length})
                      </h4>
                      {selectedRole.skill_match_details.missing_skills.slice(0, 3).map((skill, idx) => (
                        <div key={idx} style={{ marginBottom: '8px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                            <span style={{ fontWeight: '500', color: '#1f2937' }}>{skill.skill}</span>
                            <span style={{ color: '#6b7280' }}>0/{skill.required_level}</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', background: '#fee2e2', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{
                              width: '0%',
                              height: '100%',
                              background: '#ef4444',
                              borderRadius: '3px'
                            }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </>
            )}
          </div>

          {/* Right: Recommended Courses */}
          <div style={{
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            padding: '24px'
          }}>
            <h3 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
              {selectedRole ? `Courses for ${selectedRole.role.title}` : 'Recommended Courses'}
            </h3>

            {loadingCourses ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px' }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    border: '4px solid #e5e7eb',
                    borderTopColor: '#7c3aed',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                    margin: '0 auto 12px'
                  }} />
                  <p style={{ color: '#6b7280', fontSize: '14px' }}>Loading courses...</p>
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {(selectedRole && coursesData.length > 0 ? coursesData : courseRecommendations).map((course, idx) => (
                  <div
                    key={idx}
                    style={{
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      padding: '16px',
                      transition: 'border-color 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.borderColor = '#a855f7'}
                    onMouseLeave={(e) => e.currentTarget.style.borderColor = '#e5e7eb'}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '12px' }}>
                      <div style={{
                        width: '48px',
                        height: '48px',
                        background: '#7c3aed',
                        borderRadius: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                      }}>
                        <BookOpen style={{ width: '24px', height: '24px', color: 'white' }} />
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <h4 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '4px', fontSize: '14px' }}>
                          {course.title}
                        </h4>
                        <p style={{ fontSize: '12px', color: '#6b7280', marginBottom: '8px' }}>{course.level}</p>
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>{course.provider}</span>
                      <button
                        onClick={() => window.open(course.url, '_blank')}
                        style={{
                          background: '#2563eb',
                          color: 'white',
                          padding: '6px 16px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '500',
                          border: 'none',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                          transition: 'background 0.2s'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = '#1d4ed8'}
                        onMouseLeave={(e) => e.currentTarget.style.background = '#2563eb'}
                      >
                        Enroll Now <ExternalLink style={{ width: '12px', height: '12px' }} />
                      </button>
                    </div>

                    {course.tag && (
                      <div style={{ marginTop: '8px' }}>
                        <span style={{ fontSize: '12px', color: '#14b8a6' }}>{course.tag}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

export default DashboardPage;