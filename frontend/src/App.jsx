import React, { useState } from 'react';
import { 
  Sparkles, FileText, Upload, Trophy, CheckCircle2, ChevronRight, 
  BarChart3, BrainCircuit, RefreshCw, Eye, Award, FileCheck, ArrowRight, Play, Check 
} from 'lucide-react';
import confetti from 'canvas-confetti';
import CandidateModal from './components/CandidateModal';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [activeStep, setActiveStep] = useState(1);

  const [jobDescription, setJobDescription] = useState(`About the job
Location: Karachi/ Lahore/ Islamabad/ Peshawar/ Abbottabad

Work Arrangement:
 Onsite
 Hybrid
 Remote

About the Internship Program: Gain hands-on industry experience by working on real projects alongside experienced professionals while developing practical workplace skills.

Eligibility Criteria:
 Final-year students or fresh graduates
 Bachelor's or Master's students/graduates in relevant disciplines
 Strong communication and interpersonal skills
 Eager to learn and work in a professional environment

Experience Requirements:
 No prior experience required
 Internships, academic projects, volunteer work, or extracurricular activities will be a plus.`);

  const [files, setFiles] = useState([]);
  const [parsedJob, setParsedJob] = useState(null);
  const [rankings, setRankings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files).filter(
      f => f.name.toLowerCase().endsWith('.pdf') || f.type === 'application/pdf'
    );
    setFiles(selectedFiles);
  };

  const handleAnalyzeJob = async () => {
    if (!jobDescription.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/jobs/parse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: jobDescription })
      });
      const data = await res.json();
      if (res.ok) {
        setParsedJob(data.job);
        setActiveStep(2);
      }
    } catch (err) {
      console.error("Job parse error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunScreening = async () => {
    if (!files.length) {
      alert("Please upload at least one PDF resume first!");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      files.forEach(file => formData.append('files', file));

      const uploadRes = await fetch(`${API_BASE_URL}/api/v1/resume/batch-upload`, {
        method: 'POST',
        body: formData
      });

      if (!uploadRes.ok) throw new Error("Failed to process PDF resumes");

      const uploadData = await uploadRes.json();
      const resumeTexts = uploadData.resumes.map(r => r.extracted_text);

      const rankRes = await fetch(`${API_BASE_URL}/api/v1/ranking/rank`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_texts: resumeTexts,
          job_description: jobDescription
        })
      });

      if (!rankRes.ok) throw new Error("Failed to rank candidates");

      const rankData = await rankRes.json();
      setRankings(rankData);
      setActiveStep(3);

      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });

    } catch (err) {
      alert("Screening failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', flex: 1 }}>
      {/* App Header */}
      <header style={{ textAlign: 'center', marginBottom: '40px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '6px 18px', borderRadius: '9999px', background: 'rgba(99, 102, 241, 0.12)', border: '1px solid rgba(99, 102, 241, 0.3)', color: '#818cf8', fontSize: '0.875rem', fontWeight: '600', marginBottom: '16px' }}>
          <BrainCircuit size={16} /> TalentIQ AI – Intelligent Resume Screening & Candidate Ranking System
        </div>
        <h1 style={{ fontSize: '3.25rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '12px' }} className="gradient-text">
          TalentIQ AI
        </h1>
        <p style={{ color: '#9ca3af', fontSize: '1.1rem', maxWidth: '680px', margin: '0 auto' }}>
          Paste any Job Description or Internship post, upload candidate resumes, and watch AI extract, match, and rank candidates instantly.
        </p>
      </header>

      {/* Visual Workflow Steps Navigation */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '40px' }}>
        <div 
          onClick={() => setActiveStep(1)}
          className="glass-panel" 
          style={{ 
            padding: '18px 24px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '14px',
            borderColor: activeStep === 1 ? '#6366f1' : 'var(--border-color)',
            background: activeStep === 1 ? 'rgba(99, 102, 241, 0.15)' : 'var(--bg-card)'
          }}
        >
          <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: activeStep === 1 ? '#6366f1' : 'rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#fff' }}>1</div>
          <div>
            <div style={{ color: '#fff', fontWeight: '700', fontSize: '0.95rem' }}>Step 1: Job Description</div>
            <div style={{ color: '#9ca3af', fontSize: '0.8rem' }}>Paste role details & parse</div>
          </div>
        </div>

        <div 
          onClick={() => parsedJob && setActiveStep(2)}
          className="glass-panel" 
          style={{ 
            padding: '18px 24px', cursor: parsedJob ? 'pointer' : 'not-allowed', display: 'flex', alignItems: 'center', gap: '14px',
            opacity: parsedJob ? 1 : 0.6,
            borderColor: activeStep === 2 ? '#06b6d4' : 'var(--border-color)',
            background: activeStep === 2 ? 'rgba(6, 182, 212, 0.15)' : 'var(--bg-card)'
          }}
        >
          <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: activeStep === 2 ? '#06b6d4' : 'rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#fff' }}>2</div>
          <div>
            <div style={{ color: '#fff', fontWeight: '700', fontSize: '0.95rem' }}>Step 2: Upload Resumes</div>
            <div style={{ color: '#9ca3af', fontSize: '0.8rem' }}>Batch upload PDF resumes</div>
          </div>
        </div>

        <div 
          onClick={() => rankings && setActiveStep(3)}
          className="glass-panel" 
          style={{ 
            padding: '18px 24px', cursor: rankings ? 'pointer' : 'not-allowed', display: 'flex', alignItems: 'center', gap: '14px',
            opacity: rankings ? 1 : 0.6,
            borderColor: activeStep === 3 ? '#f59e0b' : 'var(--border-color)',
            background: activeStep === 3 ? 'rgba(245, 158, 11, 0.15)' : 'var(--bg-card)'
          }}
        >
          <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: activeStep === 3 ? '#f59e0b' : 'rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#fff' }}>3</div>
          <div>
            <div style={{ color: '#fff', fontWeight: '700', fontSize: '0.95rem' }}>Step 3: Ranking Results</div>
            <div style={{ color: '#9ca3af', fontSize: '0.8rem' }}>AI Leaderboard & Insights</div>
          </div>
        </div>
      </div>

      {/* STEP 1 CONTAINER */}
      {activeStep === 1 && (
        <div className="glass-panel animate-fade-in" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <h2 style={{ fontSize: '1.4rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <FileText size={24} color="#6366f1" /> Step 1 — Paste Job Description or Internship Post
              </h2>
              <p style={{ color: '#9ca3af', fontSize: '0.875rem', marginTop: '4px' }}>
                Paste any job advertisement, eligibility criteria, or internship description below.
              </p>
            </div>
            <button 
              className="btn-primary" 
              onClick={handleAnalyzeJob} 
              disabled={loading || !jobDescription.trim()}
            >
              {loading ? <RefreshCw size={18} className="animate-spin" /> : <Sparkles size={18} />}
              Analyze Job & Extract Requirements
            </button>
          </div>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste Job Description text here..."
            style={{ width: '100%', height: '280px', background: 'rgba(10, 15, 26, 0.6)', border: '1px solid var(--border-color)', borderRadius: '14px', padding: '20px', color: '#f3f4f6', fontFamily: 'var(--font-body)', fontSize: '0.95rem', lineHeight: '1.6', resize: 'vertical', outline: 'none' }}
          />

          {parsedJob && (
            <div style={{ marginTop: '24px', padding: '20px', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div style={{ fontSize: '0.9rem', color: '#818cf8', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  ✓ Parsed Job Information:
                </div>
                <button 
                  onClick={() => setActiveStep(2)}
                  style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem' }}
                >
                  Proceed to Resume Upload <ArrowRight size={16} />
                </button>
              </div>

              <div style={{ color: '#fff', fontWeight: '700', fontSize: '1.2rem', marginBottom: '8px' }}>{parsedJob.title}</div>
              <div style={{ color: '#9ca3af', fontSize: '0.9rem', marginBottom: '12px' }}>
                <strong>Experience Needed:</strong> {parsedJob.experience} • <strong>Education Criteria:</strong> {parsedJob.education}
              </div>

              {parsedJob.skills.length > 0 && (
                <div>
                  <div style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '6px' }}>Extracted Skills & Competencies:</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {parsedJob.skills.map((s, i) => (
                      <span key={i} className="pill-badge pill-indigo">{s}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* STEP 2 CONTAINER */}
      {activeStep === 2 && (
        <div className="glass-panel animate-fade-in" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <h2 style={{ fontSize: '1.4rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Upload size={24} color="#06b6d4" /> Step 2 — Upload Candidate PDF Resumes
              </h2>
              <p style={{ color: '#9ca3af', fontSize: '0.875rem', marginTop: '4px' }}>
                Select multiple candidate resumes (PDF format). PyMuPDF will extract full text instantly.
              </p>
            </div>
          </div>

          <label style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '220px', border: '2px dashed rgba(6, 182, 212, 0.4)', borderRadius: '16px', background: 'rgba(6, 182, 212, 0.04)', cursor: 'pointer', transition: 'all 0.2s ease', marginBottom: '24px' }}>
            <Upload size={48} color="#06b6d4" style={{ marginBottom: '12px' }} />
            <span style={{ color: '#f3f4f6', fontWeight: '700', fontSize: '1.1rem' }}>Click or Drag PDF Candidate Resumes Here</span>
            <span style={{ color: '#6b7280', fontSize: '0.85rem', marginTop: '6px' }}>Select 1 or multiple PDF files for batch evaluation</span>
            <input type="file" multiple accept=".pdf" onChange={handleFileChange} style={{ display: 'none' }} />
          </label>

          {files.length > 0 && (
            <div style={{ marginBottom: '28px', background: 'rgba(6, 182, 212, 0.08)', padding: '20px', borderRadius: '12px', border: '1px solid rgba(6, 182, 212, 0.2)' }}>
              <div style={{ fontSize: '0.9rem', color: '#06b6d4', fontWeight: '700', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCheck size={18} /> Selected Candidate Resumes ({files.length}):
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '10px' }}>
                {files.map((f, i) => (
                  <div key={i} style={{ background: 'rgba(255, 255, 255, 0.08)', padding: '10px 14px', borderRadius: '8px', fontSize: '0.85rem', color: '#f3f4f6', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    📄 {f.name}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button 
              onClick={() => setActiveStep(1)} 
              style={{ background: 'transparent', border: '1px solid var(--border-color)', color: '#9ca3af', padding: '12px 24px', borderRadius: '10px', cursor: 'pointer', fontWeight: '600' }}
            >
              ← Back to Job Description
            </button>

            <button 
              className="btn-primary" 
              onClick={handleRunScreening} 
              disabled={loading || !files.length}
              style={{ padding: '16px 32px', fontSize: '1rem' }}
            >
              {loading ? (
                <>
                  <RefreshCw size={20} className="animate-spin" /> Running AI Matching & Ranking Engine...
                </>
              ) : (
                <>
                  <Sparkles size={20} /> Calculate Match & Rank Candidates
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* STEP 3 CONTAINER: RANKING DASHBOARD */}
      {activeStep === 3 && rankings && (
        <div className="glass-panel animate-fade-in" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <div>
              <h2 style={{ fontSize: '1.6rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Trophy size={28} color="#f59e0b" /> Candidate Ranking Leaderboard
              </h2>
              <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
                Evaluated Job Role: <span style={{ color: '#fff', fontWeight: '700' }}>{rankings.job_title}</span> • Total Candidates Scored: <span style={{ color: '#818cf8', fontWeight: '700' }}>{rankings.total_candidates}</span>
              </p>
            </div>

            <button 
              onClick={() => setActiveStep(1)}
              style={{ background: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', color: '#818cf8', padding: '10px 18px', borderRadius: '10px', cursor: 'pointer', fontWeight: '600', fontSize: '0.85rem' }}
            >
              + Start New Screening Session
            </button>
          </div>

          {/* Leaderboard Table */}
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: '#9ca3af', fontSize: '0.85rem', textTransform: 'uppercase' }}>
                  <th style={{ padding: '14px' }}>Rank</th>
                  <th style={{ padding: '14px' }}>Candidate Name</th>
                  <th style={{ padding: '14px' }}>Overall AI Match</th>
                  <th style={{ padding: '14px' }}>Skill Match</th>
                  <th style={{ padding: '14px' }}>Matched Skills</th>
                  <th style={{ padding: '14px', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {rankings.rankings.map((cand, idx) => {
                  const scorePct = Math.round(cand.scores.overall_score * 100);
                  const skillPct = Math.round(cand.scores.skill_match * 100);

                  return (
                    <tr 
                      key={idx} 
                      style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)', transition: 'background 0.2s' }}
                      onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'}
                      onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                    >
                      <td style={{ padding: '16px', fontSize: '1.25rem', fontWeight: 'bold' }}>
                        {getRankBadge(cand.rank)}
                      </td>
                      <td style={{ padding: '16px' }}>
                        <div style={{ color: '#fff', fontWeight: '600', fontSize: '1rem' }}>{cand.candidate_name || 'Candidate Profile'}</div>
                        <div style={{ color: '#6b7280', fontSize: '0.8rem' }}>{cand.email || 'No email specified'}</div>
                      </td>
                      <td style={{ padding: '16px', width: '220px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.85rem', fontWeight: '700', color: scorePct >= 75 ? '#34d399' : '#818cf8' }}>
                          <span>{scorePct}% Match</span>
                        </div>
                        <div className="progress-bar-bg">
                          <div 
                            className="progress-bar-fill" 
                            style={{ 
                              width: `${scorePct}%`, 
                              background: scorePct >= 75 ? 'linear-gradient(90deg, #10b981, #34d399)' : 'linear-gradient(90deg, #6366f1, #06b6d4)' 
                            }} 
                          />
                        </div>
                      </td>
                      <td style={{ padding: '16px', fontWeight: '600', color: '#f59e0b' }}>
                        {skillPct}%
                      </td>
                      <td style={{ padding: '16px' }}>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                          {cand.skill_analysis.matched_skills.slice(0, 3).map((s, i) => (
                            <span key={i} className="pill-badge pill-emerald" style={{ fontSize: '0.75rem', padding: '2px 8px' }}>{s}</span>
                          ))}
                          {cand.skill_analysis.matched_skills.length > 3 && (
                            <span style={{ color: '#9ca3af', fontSize: '0.75rem', alignSelf: 'center' }}>+{cand.skill_analysis.matched_skills.length - 3} more</span>
                          )}
                        </div>
                      </td>
                      <td style={{ padding: '16px', textAlign: 'right' }}>
                        <button 
                          onClick={() => setSelectedCandidate(cand)}
                          style={{ background: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', color: '#818cf8', padding: '8px 14px', borderRadius: '8px', fontSize: '0.85rem', fontWeight: '600', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                        >
                          <Eye size={14} /> View AI Candidate Details
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Candidate Details Modal */}
      {selectedCandidate && (
        <CandidateModal candidate={selectedCandidate} onClose={() => setSelectedCandidate(null)} />
      )}
    </div>
  );
}
