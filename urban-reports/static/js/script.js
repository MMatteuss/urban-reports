// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Photo upload preview
    const photoInput = document.getElementById('photos');
    const previewContainer = document.getElementById('photo-preview');
    
    if (photoInput && previewContainer) {
        photoInput.addEventListener('change', function() {
            previewContainer.innerHTML = '';
            
            for (let i = 0; i < this.files.length; i++) {
                const file = this.files[i];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'photo-preview';
                    img.alt = 'Preview ' + (i + 1);
                    previewContainer.appendChild(img);
                }
                
                reader.readAsDataURL(file);
            }
        });
    }

    // Location detection
    const getLocationBtn = document.getElementById('get-location');
    if (getLocationBtn) {
        getLocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                Swal.fire({
                    title: 'Obtendo localização...',
                    text: 'Por favor, aguarde.',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        document.getElementById('latitude').value = position.coords.latitude;
                        document.getElementById('longitude').value = position.coords.longitude;
                        
                        // Reverse geocoding (you would use a proper geocoding service in production)
                        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('address').value = data.display_name;
                                Swal.close();
                                Swal.fire({
                                    title: 'Localização obtida!',
                                    text: 'Endereço preenchido automaticamente.',
                                    icon: 'success',
                                    timer: 2000
                                });
                            });
                    },
                    function(error) {
                        Swal.close();
                        Swal.fire({
                            title: 'Erro!',
                            text: 'Não foi possível obter a localização.',
                            icon: 'error'
                        });
                    }
                );
            } else {
                Swal.fire({
                    title: 'Erro!',
                    text: 'Geolocalização não suportada pelo navegador.',
                    icon: 'error'
                });
            }
        });
    }

    // Vote system
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const reportId = this.dataset.reportId;
            const voteType = this.dataset.voteType;
            
            fetch(`/report/${reportId}/vote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `type=${voteType}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        });
    });

    // Report search
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const query = document.getElementById('search-query').value.trim();
            if (!query) {
                e.preventDefault();
                Swal.fire({
                    title: 'Campo vazio',
                    text: 'Por favor, digite algo para buscar.',
                    icon: 'warning'
                });
            }
        });
    }

    // Auto-refresh for new reports (every 30 seconds on dashboard)
    if (window.location.pathname === '/dashboard') {
        setInterval(() => {
            fetch('/api/reports')
                .then(response => response.json())
                .then(data => {
                    // Update report count
                    const newReports = data.filter(report => {
                        const reportTime = new Date(report.created_at);
                        const now = new Date();
                        return (now - reportTime) < 30000; // Last 30 seconds
                    });
                    
                    if (newReports.length > 0) {
                        Swal.fire({
                            title: 'Novos Reportes!',
                            text: `${newReports.length} novo(s) reporte(s) disponível(is).`,
                            icon: 'info',
                            timer: 3000
                        });
                    }
                });
        }, 30000); // 30 seconds
    }

    // Markdown preview for descriptions
    const descriptionInput = document.getElementById('description');
    const previewArea = document.getElementById('description-preview');
    
    if (descriptionInput && previewArea) {
        descriptionInput.addEventListener('input', function() {
            // Simple markdown conversion
            let text = this.value;
            
            // Headers
            text = text.replace(/^### (.*$)/gm, '<h3>$1</h3>');
            text = text.replace(/^## (.*$)/gm, '<h2>$1</h2>');
            text = text.replace(/^# (.*$)/gm, '<h1>$1</h1>');
            
            // Bold
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            // Italic
            text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
            
            // Line breaks
            text = text.replace(/\n/g, '<br>');
            
            // Links
            text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
            
            previewArea.innerHTML = text;
        });
    }

    // Image modal
    document.querySelectorAll('.report-image').forEach(img => {
        img.addEventListener('click', function() {
            Swal.fire({
                imageUrl: this.src,
                imageAlt: 'Report Image',
                showCloseButton: true,
                showConfirmButton: false,
                width: '80%'
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR');
}

function getCategoryColor(category) {
    const colors = {
        'buraco': 'bg-buraco',
        'esgoto': 'bg-esgoto',
        'lixo': 'bg-lixo',
        'poste': 'bg-poste',
        'outros': 'bg-outros'
    };
    return colors[category] || 'bg-secondary';
}

// Export for use in other scripts
window.UrbanReports = {
    formatDate,
    getCategoryColor
};