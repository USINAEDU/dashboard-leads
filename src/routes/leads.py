from flask import Blueprint, jsonify
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import json
import plotly

leads_bp = Blueprint('leads', __name__)

def get_data_path(filename):
    """Get the path to data files in the static folder"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', filename)

@leads_bp.route('/leads-data')
def get_leads_data():
    """Get leads data for dashboard"""
    try:
        # Load leads data
        leads_df = pd.read_csv(get_data_path('leads_final_cleaned.csv'))
        
        # Basic statistics
        total_leads = len(leads_df)
        
        # Profession distribution
        profession_counts = leads_df['Profissão'].value_counts().head(10)
        
        # Student quantity distribution
        student_counts = leads_df['Quantidade de Alunos'].value_counts()
        
        # Product value distribution
        value_counts = leads_df['Valor do Produto'].value_counts()
        
        # Origin distribution
        origin_counts = leads_df['Origem'].value_counts().head(10)
        
        # Product interest distribution
        product_interest_counts = leads_df['Produto de interesse'].value_counts()
        
        return jsonify({
            'total_leads': total_leads,
            'profession_distribution': profession_counts.to_dict(),
            'student_quantity_distribution': student_counts.to_dict(),
            'product_value_distribution': value_counts.to_dict(),
            'origin_distribution': origin_counts.to_dict(),
            'product_interest_distribution': product_interest_counts.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/clients-data')
def get_clients_data():
    """Get clients data for dashboard"""
    try:
        # Load clients data
        clients_df = pd.read_csv(get_data_path('clients_cleaned.csv'))
        
        # Basic statistics
        total_clients = len(clients_df)
        
        # Classification distribution
        classification_counts = clients_df['Classificação'].value_counts()
        
        # Status distribution
        status_counts = clients_df['Status do Cliente'].value_counts()
        
        # Product usage
        extension_usage = clients_df['Extensão'].value_counts()
        pos_grad_usage = clients_df['Pós-graduação'].value_counts()
        
        return jsonify({
            'total_clients': total_clients,
            'classification_distribution': classification_counts.to_dict(),
            'status_distribution': status_counts.to_dict(),
            'extension_usage': extension_usage.to_dict(),
            'pos_graduation_usage': pos_grad_usage.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/performance-data')
def get_performance_data():
    """Get performance data for dashboard"""
    try:
        # Load performance data
        performance_df = pd.read_csv(get_data_path('dashboard_performance_leads.csv'))
        
        # Convert to proper format for charts
        performance_data = performance_df.to_dict('records')
        
        return jsonify({
            'performance_data': performance_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/conversion-analysis')
def get_conversion_analysis():
    """Get conversion analysis data"""
    try:
        # Load both datasets
        leads_df = pd.read_csv(get_data_path('leads_final_cleaned.csv'))
        clients_df = pd.read_csv(get_data_path('clients_cleaned.csv'))
        
        # Merge to find converted leads
        merged_df = pd.merge(leads_df, clients_df, left_on='Email', right_on='E-mail', how='inner')
        
        # Conversion by profession
        conversion_by_profession = merged_df['Profissão'].value_counts()
        
        # Conversion by student quantity
        conversion_by_students = merged_df['Quantidade de Alunos'].value_counts()
        
        # Conversion by product value
        conversion_by_value = merged_df['Valor do Produto'].value_counts()
        
        return jsonify({
            'total_conversions': len(merged_df),
            'conversion_rate': (len(merged_df) / len(leads_df)) * 100,
            'conversion_by_profession': conversion_by_profession.to_dict(),
            'conversion_by_students': conversion_by_students.to_dict(),
            'conversion_by_value': conversion_by_value.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/charts/profession-distribution')
def get_profession_chart():
    """Get profession distribution chart"""
    try:
        leads_df = pd.read_csv(get_data_path('leads_final_cleaned.csv'))
        profession_counts = leads_df['Profissão'].value_counts().head(10)
        
        fig = px.bar(
            x=profession_counts.values,
            y=profession_counts.index,
            orientation='h',
            title='Distribuição de Leads por Profissão',
            labels={'x': 'Quantidade de Leads', 'y': 'Profissão'}
        )
        fig.update_layout(height=500)
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'chart': graphJSON})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/charts/conversion-funnel')
def get_conversion_funnel():
    """Get conversion funnel chart"""
    try:
        leads_df = pd.read_csv(get_data_path('leads_final_cleaned.csv'))
        clients_df = pd.read_csv(get_data_path('clients_cleaned.csv'))
        
        total_leads = len(leads_df)
        total_clients = len(clients_df)
        
        # Create funnel chart
        fig = go.Figure(go.Funnel(
            y = ["Total de Leads", "Leads Convertidos"],
            x = [total_leads, total_clients],
            textinfo = "value+percent initial"
        ))
        
        fig.update_layout(title="Funil de Conversão de Leads")
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'chart': graphJSON})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

