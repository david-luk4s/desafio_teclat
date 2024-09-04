
// Evento Submit para salvar Tarefa
document.getElementById('taskForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário tradicional

    // Captura os valores dos inputs
    const taskName = document.getElementById('taskName').value;
    const taskDescription = document.getElementById('taskDescription').value;

    // Faz uma requisição POST usando fetch
    fetch('/api/add_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            taskName: taskName,
            taskDescription: taskDescription
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Atualiza a tabela com a nova tarefa
        const taskTableBody = document.getElementById('taskTableBody');
        const newRow = document.createElement('tr');
        newRow.setAttribute('data-task-id', data.id);

        newRow.innerHTML = `
            <td>
                <input type="text" value="${data.titulo}" disabled>
            </td>
            <td>
                <textarea disabled>${data.descricao}</textarea>
            </td>
            <td>
                <select disabled>
                    <option value="Pendente" ${!data.status_conclusao ? 'selected' : ''}>Pendente</option>
                    <option value="Concluída" ${data.status_conclusao ? 'selected' : ''}>Concluída</option>
                </select>
            </td>
            <td>${new Date(data.data_criacao).toLocaleString('pt-BR')}</td>
            <td>
                ${data.data_status_conclusao ? new Date(data.data_status_conclusao).toLocaleString('pt-BR') : '-'}
            </td>
            <td>
                <button class="edit-btn">Editar</button>
                <button class="save-btn" disabled>Salvar</button>
                <button class="delete-btn">Deletar</button>
            </td>
        `;
        taskTableBody.appendChild(newRow);

        // Limpar campos
        document.getElementById('taskForm').reset();

        // Exibe uma mensagem de sucesso
        document.getElementById('message').textContent = 'Tarefa adicionada com sucesso!';
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Erro ao adicionar a tarefa.';
        console.error('Erro:', error);
    });
});


// Evento Click para Editar Tarefas
document.getElementById('taskTableBody').addEventListener('click', function(event) {
    if (event.target.classList.contains('edit-btn')) {
        const row = event.target.closest('tr');
        const inputs = row.querySelectorAll('input, textarea, select');
        const saveBtn = row.querySelector('.save-btn');

        inputs.forEach(input => input.removeAttribute('disabled'));
        saveBtn.removeAttribute('disabled');
        event.target.setAttribute('disabled', 'true');
    } else if (event.target.classList.contains('save-btn')) {
        const row = event.target.closest('tr');
        const inputs = row.querySelectorAll('input, textarea, select');
        const editBtn = row.querySelector('.edit-btn');

        const taskId = row.getAttribute('data-task-id');
        const taskTitle = inputs[0].value.trim();
        const taskDescription = inputs[1].value.trim();
        const taskStatus = inputs[2].value === 'Concluída';

        // Enviar os dados atualizados para o servidor via fetch API
        fetch(`/api/update_task/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                taskTitle: taskTitle,
                taskDescription: taskDescription,
                taskStatus: taskStatus
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Desabilitar edição novamente
            inputs.forEach(input => input.setAttribute('disabled', 'true'));
            event.target.setAttribute('disabled', 'true');
            editBtn.removeAttribute('disabled');
            
            // Atualizar a data de conclusão se necessário
            const dateCell = row.querySelectorAll('td')[4];
            if (taskStatus) {
                dateCell.innerText = data.data_status_conclusao;
            } else {
                dateCell.innerText = '-';
            }

            document.getElementById('message').textContent = 'Tarefa atualizada com sucesso!';
        })
        .catch(error => {
            document.getElementById('message').textContent = 'Erro ao atualizar a tarefa.';
            console.error('Erro:', error);
        });
    }
});

// Evento Click para deletar Tarefas
document.getElementById('taskTableBody').addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-btn')) {
        const row = event.target.closest('tr');
        const taskId = row.getAttribute('data-task-id');

        fetch(`/api/delete_task/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                // A resposta foi bem-sucedida (status 200-299)
                return response.json(); // Converte a resposta em JSON
            } else {
                // Se a resposta não for bem-sucedida, lança um erro
                return response.text().then(text => {
                    throw new Error(`Erro ao excluir a tarefa. Status: ${response.status}, Mensagem: ${text}`);
                });
            }
        })
        .then(data => {
            // Se o JSON for retornado e o status for OK
            row.remove();
            document.getElementById('message').textContent = 'Tarefa excluída com sucesso!';
        })
        .catch(error => {
            // Trata erros na requisição e resposta
            document.getElementById('message').textContent = error.message;
            console.error('Erro:', error);
        });
    }
});