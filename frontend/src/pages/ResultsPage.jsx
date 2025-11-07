import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Brain, Upload, FileText, ChevronRight, Briefcase, BookOpen, ExternalLink } from 'lucide-react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { resumeAPI, rolesAPI } from '../services/api';

const ResultsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [uploadError] = useState(null);

  // Collapsible sections state
  const [expandedSections, setExpandedSections] = useState({
    summary: false,
    workHistory: false,
    skills: true,
    education: false
  });

  useEffect(() => {
    fetchResults();
  }, [id]);

  const fetchResults = async () => {
    try {
      setLoading(true);

      // Get parsed resume
      const resumeResponse = await resumeAPI.getParsed(id);
      setResumeData(resumeResponse);

      // Get recommendations
      const recData = await rolesAPI.getRecommendations(id, 5);
      setRecommendations(recData);

    } catch (err) {
      console.error('Error fetching results:', err);
      setError(err.message);
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

  const handleFileUpload = async (file) => {
    try {
      setLoading(true);
      const response = await resumeAPI.upload(file);
      if (response.resume_id) {
        navigate(`/results/${response.resume_id}`);
      }
    } catch (error) {
      setError('Failed to upload resume');
    } finally {
      setLoading(false);
    }
  };

  // Prepare radar chart data
  const getRadarChartData = () => {
    if (!recommendations?.recommendations?.[0]) return [];

    return [
      { skill: 'Python', value: 4, fullMark: 5 },
      { skill: 'Pandas', value: 2, fullMark: 5 },
      { skill: 'Machine Learning', value: 3, fullMark: 5 },
      { skill: 'SQL', value: 2, fullMark: 5 },
      { skill: 'Statistics', value: 3, fullMark: 5 },
      { skill: 'Visualization', value: 1, fullMark: 5 }
    ];
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
      padding: '24px'
    }}>
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
            <div style={{
              width: '100%',
              maxWidth: '448px',
              border: '2px dashed #d1d5db',
              borderRadius: '12px',
              padding: '48px',
              textAlign: 'center',
              cursor: 'pointer',
              transition: 'border-color 0.2s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.borderColor = '#14b8a6'}
            onMouseLeave={(e) => e.currentTarget.style.borderColor = '#d1d5db'}
            >
              <input
                type="file"
                accept=".pdf,.docx,.doc,.txt"
                style={{ display: 'none' }}
                id="resume-upload"
                onChange={(e) => {
                  const file = e.target.files[0];
                  if (file) {
                    handleFileUpload(file);
                  }
                }}
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

            {error && (
              <div style={{
                marginTop: '16px',
                width: '100%',
                maxWidth: '448px',
                background: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                padding: '12px'
              }}>
                <p style={{ color: '#dc2626', fontSize: '14px' }}>An error occurred while processing your resume</p>
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
        </div>
      </div>

      {/* Bottom Section - Three Columns */}
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
            {recommendations?.recommendations?.slice(0, 2).map((rec, idx) => (
              <div
                key={idx}
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  padding: '16px',
                  transition: 'border-color 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = '#14b8a6'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = '#e5e7eb'}
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

          {recommendations?.recommendations?.length > 2 && (
            <button
              onClick={() => {}}
              style={{
                width: '100%',
                marginTop: '16px',
                color: '#14b8a6',
                fontWeight: '500',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '4px',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                padding: '8px'
              }}
            >
              View All Roles <ChevronRight style={{ width: '16px', height: '16px' }} />
            </button>
          )}
        </div>

        {/* Center: Skill Gap Visualization */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          padding: '24px'
        }}>
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
        </div>

        {/* Right: Recommended Courses */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          padding: '24px'
        }}>
          <h3 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', marginBottom: '16px' }}>
            Recommended Courses
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {courseRecommendations.map((course, idx) => (
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
                  <button style={{
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

                <div style={{ marginTop: '8px' }}>
                  <span style={{ fontSize: '12px', color: '#14b8a6' }}>{course.tag}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;