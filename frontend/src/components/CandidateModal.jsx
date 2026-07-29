import React from 'react';
import { X, CheckCircle2, AlertCircle, Award, Briefcase, GraduationCap, Sparkles, User, Mail, Phone } from 'lucide-react';

export default function CandidateModal({ candidate, onClose }) {
  if (!candidate) return null;

  const scorePct = Math.round(candidate.scores.overall_score * 100);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="glass-panel animate-fade-in" 
        style={{ width: '100%', maxWidth: '750px', maxHeight: '90vh', overflowY: 'auto', padding: '32px', position: 'relative' }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button 
          onClick={onClose}
          style={{ position: 'absolute', top: '24px', right: '24px', background: 'transparent', border: 'none', color: '#9ca3af', cursor: 'pointer' }}
        >
          <X size={24} />
        </button>

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '24px' }}>
          <div style={{ 
            width: '64px', height: '64px', borderRadius: '16px', 
            background: 'linear-gradient(135deg, #6366f1 0%, #06b6d4 100%)', 
            display: 'flex', alignItems: 'center', justifyContent: 'center', 
            fontSize: '1.5rem', fontWeight: 'bold', color: '#fff' 
          }}>
            #{candidate.rank}
          </div>
          <div>
            <h2 style={{ fontSize: '1.75rem', color: '#fff', marginBottom: '4px' }}>{candidate.candidate_name || 'Candidate Profile'}</h2>
            <div style={{ display: 'flex', gap: '16px', color: '#9ca3af', fontSize: '0.875rem' }}>
              {candidate.email && <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><Mail size={14} /> {candidate.email}</span>}
              {candidate.phone && <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><Phone size={14} /> {candidate.phone}</span>}
            </div>
          </div>
        </div>

        {/* Overall Score Banner */}
        <div style={{ 
          background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)', 
          borderRadius: '16px', padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          marginBottom: '28px'
        }}>
          <div>
            <div style={{ color: '#818cf8', fontWeight: '600', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Overall AI Match</div>
            <div style={{ color: '#9ca3af', fontSize: '0.875rem', marginTop: '4px' }}>{candidate.explanation.summary}</div>
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#818cf8' }}>
            {scorePct}%
          </div>
        </div>

        {/* Why this candidate? (Explainable AI Section) */}
        <div style={{ marginBottom: '28px' }}>
          <h3 style={{ fontSize: '1.1rem', color: '#f3f4f6', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <Sparkles size={18} color="#6366f1" /> Why this candidate? (Explainable AI Insights)
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {candidate.explanation.highlights.map((item, idx) => (
              <div key={idx} style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '10px', padding: '12px 16px', color: '#34d399', fontSize: '0.9rem', display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
                <CheckCircle2 size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{item}</span>
              </div>
            ))}
            {candidate.explanation.missing_points.map((item, idx) => (
              <div key={idx} style={{ background: 'rgba(244, 63, 94, 0.08)', border: '1px solid rgba(244, 63, 94, 0.2)', borderRadius: '10px', padding: '12px 16px', color: '#fb7185', fontSize: '0.9rem', display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
                <AlertCircle size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Score Breakdown Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '28px' }}>
          <div className="glass-panel" style={{ padding: '14px', textAlign: 'center' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Skill Match (40%)</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#34d399', marginTop: '4px' }}>{Math.round(candidate.scores.skill_match * 100)}%</div>
          </div>
          <div className="glass-panel" style={{ padding: '14px', textAlign: 'center' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Semantic AI (35%)</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#818cf8', marginTop: '4px' }}>{Math.round(candidate.scores.semantic_similarity * 100)}%</div>
          </div>
          <div className="glass-panel" style={{ padding: '14px', textAlign: 'center' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Experience (15%)</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#f59e0b', marginTop: '4px' }}>{Math.round(candidate.scores.experience_score * 100)}%</div>
          </div>
          <div className="glass-panel" style={{ padding: '14px', textAlign: 'center' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Education (10%)</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#06b6d4', marginTop: '4px' }}>{Math.round(candidate.scores.education_score * 100)}%</div>
          </div>
        </div>

        {/* Matched vs Missing Skills */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '28px' }}>
          <div>
            <h4 style={{ fontSize: '0.95rem', color: '#34d399', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <CheckCircle2 size={16} /> Matched Skills ({candidate.skill_analysis.matched_skills.length})
            </h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {candidate.skill_analysis.matched_skills.map((skill, idx) => (
                <span key={idx} className="pill-badge pill-emerald">{skill}</span>
              ))}
              {candidate.skill_analysis.matched_skills.length === 0 && <span style={{ color: '#6b7280', fontSize: '0.85rem' }}>None matched</span>}
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', color: '#fb7185', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <AlertCircle size={16} /> Missing Skills ({candidate.skill_analysis.missing_skills.length})
            </h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {candidate.skill_analysis.missing_skills.map((skill, idx) => (
                <span key={idx} className="pill-badge pill-rose">{skill}</span>
              ))}
              {candidate.skill_analysis.missing_skills.length === 0 && <span style={{ color: '#34d399', fontSize: '0.85rem' }}>All required skills matched!</span>}
            </div>
          </div>
        </div>

        {/* Experience & Education Details */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="glass-panel" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#f59e0b', fontSize: '0.875rem', fontWeight: '600', marginBottom: '6px' }}>
              <Briefcase size={16} /> Experience Found
            </div>
            <div style={{ color: '#f3f4f6', fontSize: '0.95rem' }}>{candidate.experience_found || 'Not specified'}</div>
          </div>

          <div className="glass-panel" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#06b6d4', fontSize: '0.875rem', fontWeight: '600', marginBottom: '6px' }}>
              <GraduationCap size={16} /> Education Found
            </div>
            <div style={{ color: '#f3f4f6', fontSize: '0.95rem' }}>{candidate.education_found || 'Not specified'}</div>
          </div>
        </div>

      </div>
    </div>
  );
}
