import React from 'react';
import ReactMarkdown from 'react-markdown';
import { FileText } from 'lucide-react';

interface ReportViewerProps {
  relatorio: string;
}

export const ReportViewer: React.FC<ReportViewerProps> = ({ relatorio }) => {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <FileText className="panel-title-icon" size={16} />
          Parecer Técnico do Modelo
        </span>
        <span className="badge-outline">Llama 3.3 70B</span>
      </div>

      <div className="markdown-body">
        <ReactMarkdown>{relatorio}</ReactMarkdown>
      </div>
    </div>
  );
};
