import sqlite3
import datetime
import os
import shutil
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_javascript import st_javascript

DB_NAME = "visitor_stats.db"
BACKUP_DB_NAME = "visitor_stats_backup.db"
INITIAL_COUNT = 28264

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_date DATE NOT NULL,
            visit_time TIME NOT NULL,
            is_new INTEGER NOT NULL
        )
    ''')
    
    # Check if we need to insert initial dummy data
    c.execute('SELECT COUNT(*) FROM visits')
    count = c.fetchone()[0]
    if count == 0:
        # We can either insert 28264 rows, or just use a baseline.
        # Inserting a single row to represent the past, or just handling INITIAL_COUNT in queries.
        pass
        
    conn.commit()
    conn.close()

def backup_db():
    if os.path.exists(DB_NAME):
        shutil.copy2(DB_NAME, BACKUP_DB_NAME)

def log_visit(is_new):
    if 'visit_logged' not in st.session_state:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        now = datetime.datetime.now()
        c.execute('INSERT INTO visits (visit_date, visit_time, is_new) VALUES (?, ?, ?)',
                  (now.date().strftime('%Y-%m-%d'), now.time().strftime("%H:%M:%S"), 1 if is_new else 0))
        conn.commit()
        conn.close()
        backup_db()
        st.session_state['visit_logged'] = True
        get_stats.clear()

@st.cache_data(ttl=60)
def get_stats():
    conn = sqlite3.connect(DB_NAME)
    
    # Total visits
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM visits')
    db_total = c.fetchone()[0]
    total_visits = INITIAL_COUNT + db_total
    
    # Today's visits
    today = datetime.date.today()
    c.execute('SELECT COUNT(*) FROM visits WHERE visit_date = ?', (today.strftime('%Y-%m-%d'),))
    today_visits = c.fetchone()[0]
    
    # Yesterday's visits for growth rate
    yesterday = today - datetime.timedelta(days=1)
    c.execute('SELECT COUNT(*) FROM visits WHERE visit_date = ?', (yesterday.strftime('%Y-%m-%d'),))
    yesterday_visits = c.fetchone()[0]
    
    # This week's visits
    start_of_week = today - datetime.timedelta(days=today.weekday())
    c.execute('SELECT COUNT(*) FROM visits WHERE visit_date >= ?', (start_of_week.strftime('%Y-%m-%d'),))
    week_visits = c.fetchone()[0]
    
    # Trend data (last 7 days)
    seven_days_ago = today - datetime.timedelta(days=6)
    query = 'SELECT visit_date, COUNT(*) as count FROM visits WHERE visit_date >= ? GROUP BY visit_date ORDER BY visit_date'
    df_trend = pd.read_sql_query(query, conn, params=(seven_days_ago.strftime('%Y-%m-%d'),))
    conn.close()
    
    # Calculate growth rate
    if yesterday_visits == 0:
        growth_rate = 100.0 if today_visits > 0 else 0.0
    else:
        growth_rate = ((today_visits - yesterday_visits) / yesterday_visits) * 100
        
    # Fill missing days in trend
    date_list = [seven_days_ago + datetime.timedelta(days=x) for x in range(7)]
    df_dates = pd.DataFrame({'visit_date': [d.strftime('%Y-%m-%d') for d in date_list]})
    if not df_trend.empty:
        df_trend = pd.merge(df_dates, df_trend, on='visit_date', how='left').fillna(0)
    else:
        df_trend = df_dates
        df_trend['count'] = 0
        
    return total_visits, today_visits, week_visits, growth_rate, df_trend

def render_visitor_counter():
    # Initialize DB
    init_db()
    
    # JS to check local storage
    js_code = """
    (function() {
        var status = "unknown";
        if (!window.sessionStorage.getItem('concrete_session_visited')) {
            window.sessionStorage.setItem('concrete_session_visited', 'true');
            if (!window.localStorage.getItem('concrete_app_visited')) {
                window.localStorage.setItem('concrete_app_visited', 'true');
                status = "new";
            } else {
                status = "recurring";
            }
        } else {
            status = "already_counted";
        }
        return status;
    })()
    """
    visitor_status = st_javascript(js_code)
    
    # log_visit if JS returned a valid status
    if visitor_status in ["new", "recurring"]:
        is_new = (visitor_status == "new")
        log_visit(is_new)
        
    # Get stats
    total, today, week, growth, df_trend = get_stats()
    
    # UI Design
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        .counter-container {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(145deg, #ffffff, #f0f8f1);
            border-radius: 15px;
            padding: 25px;
            margin-top: 40px;
            margin-bottom: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid #e0e0e0;
        }
        .counter-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.12);
        }
        .stat-box {
            text-align: center;
            padding: 20px 10px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            border-bottom: 3px solid transparent;
        }
        .stat-box:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 15px rgba(0,0,0,0.08);
            border-bottom: 3px solid #4CAF50;
        }
        .stat-value {
            font-size: 28px;
            font-weight: 600;
            color: #2e7d32;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 13px;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 400;
        }
        .growth-positive {
            color: #4caf50;
            font-weight: 600;
        }
        .growth-negative {
            color: #ff9800;
            font-weight: 600;
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .counter-container {
                background: linear-gradient(145deg, #1e1e1e, #1a251e);
                border: 1px solid #333;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            }
            .stat-box {
                background: #252525;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }
            .stat-value {
                color: #81c784;
            }
            .stat-label {
                color: #bbb;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="counter-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4CAF50; margin-bottom: 25px; font-weight: 600; letter-spacing: 0.5px;'>📊 Panel de Estadísticas de Visitas</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{total:,}</div>
                <div class="stat-label">Visitas Totales</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{today:,}</div>
                <div class="stat-label">Visitas Hoy</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{week:,}</div>
                <div class="stat-label">Esta Semana</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        growth_class = "growth-positive" if growth >= 0 else "growth-negative"
        growth_sign = "+" if growth >= 0 else ""
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value"><span class='{growth_class}'>{growth_sign}{growth:.1f}%</span></div>
                <div class="stat-label">Crecimiento (vs Ayer)</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trend Chart
    fig = px.line(df_trend, x='visit_date', y='count', 
                  title='Tendencia de Visitas (Últimos 7 días)',
                  labels={'visit_date': 'Fecha', 'count': 'Número de Visitas'},
                  markers=True)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Arial, sans-serif"),
        title_font=dict(size=18, color='#2e7d32'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
    )
    fig.update_traces(line_color='#2e7d32', line_width=3, marker=dict(size=8, color='#ff9800'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
