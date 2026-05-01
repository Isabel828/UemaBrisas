import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, Plus } from 'lucide-react';
import { dbService } from '../../services/databaseService';
import { User, REURBProcess } from '../../types/index';
import { ProcessTable } from './ProcessTable';
import { isAdmin } from '../../utils/permissoes';

export const Dashboard: React.FC<{ user: User }> = ({ user }) => {
  const [processes, setProcesses] = useState<REURBProcess[]>([]);
  const [showNotificacoes, setShowNotificacoes] = useState(false);
  const notificacoesRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Garante reconhecimento do admin mesmo se o backend mandar só name/username
  const admin =
    isAdmin(user) ||
    user?.username === "admin" ||
    user?.name === "admin";

  useEffect(() => {
    setProcesses(dbService.processes.selectAll());
  }, []);

  return (
    <div className="p-10">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-bold">
            Bem-vindo, {user?.name?.split(" ")[0] || user?.username || "usuário"}
          </h2>

          {admin && (
            <p className="text-xs text-blue-600 font-bold mt-1">
              Acesso administrativo
            </p>
          )}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setShowNotificacoes(!showNotificacoes)}
            className="relative p-3 border rounded"
          >
            <Bell />
          </button>

          {admin && (
            <button
              onClick={() => navigate('/new-process')}
              className="bg-blue-600 text-white px-4 py-2 rounded flex items-center gap-2"
            >
              <Plus size={18} /> Novo Processo
            </button>
          )}
        </div>
      </header>

      <ProcessTable processes={processes} user={user} />
    </div>
  );
};