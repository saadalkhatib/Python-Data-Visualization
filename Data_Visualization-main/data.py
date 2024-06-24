import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
from fpdf import FPDF
import os

# Funktion zur Bereinigung der Daten
def clean_data(df):
    df = df.dropna()
    df = df[df['number'] > 0] 
    return df

# Balkendiagramm
def plot_bar_chart(df):
    df['year'] = df['year'].astype('str')
    
    plt.figure(figsize=(10,6))
    plt.bar(df['year'], df["number"], color='skyblue')
    
    plt.title("Anzahl der Brände in deutschen Bundesländern von 2000 bis 2024")
    plt.xlabel("Jahr")
    plt.ylabel("Anzahl der Fälle")
    
    plt.xticks(rotation=45)
    plt.tight_layout()

# Interaktives Balkendiagramm mit Plotly
def plot_interactive_bar_chart(df):
    fig = px.bar(df, x='year', y='number', title='Anzahl der Brände in deutschen Bundesländern von 2000 bis 2024')
    fig.show()

# Tortendiagramm
def plot_pie_chart(dt):
    plt.figure(figsize=(8,8))
    plt.pie(dt['number'], labels=dt['region'], autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    plt.title("Anzahl der Brände in den deutschen Bundesländern von 2000 bis 2024")

# Interaktives Tortendiagramm mit Plotly
def plot_interactive_pie_chart(dt):
    fig = px.pie(dt, values='number', names='region', title='Anzahl der Brände in den deutschen Bundesländern von 2000 bis 2024')
    fig.show()

# Zeitliches Diagramm
def plot_time_series(data):
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    
    fig, ax = plt.subplots(figsize=(12,8))
    
    for state, state_data in data.groupby('state'):
        ax.plot(state_data['year'], state_data['number'], label=state)
    
    ax.set_xlabel('Datum')
    ax.set_ylabel('Anzahl der Fälle')
    ax.set_title('Brände in deutschen Bundesländern von 2000 bis 2024')
    ax.legend()
    

# Interaktives Zeitdiagramm mit Plotly
def plot_interactive_time_series(data):
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    
    fig = px.line(data, x='year', y='number', color='state', title='Brände in deutschen Bundesländern von 2000 bis 2024')
    fig.show()

# Speichern der Diagramme
def save_plots(df, dt, data):
    df['year'] = df['year'].astype('str')
    
    # Balkendiagramm speichern
    plt.figure(figsize=(10,6))
    plt.bar(df['year'], df["number"], color='skyblue')
    plt.title("Anzahl der Brände in deutschen Bundesländern von 2000 bis 2024")
    plt.xlabel("Jahr")
    plt.ylabel("Anzahl der Fälle")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('balkendiagramm.png')
    plt.close()
    
    # Tortendiagramm speichern
    plt.figure(figsize=(8,8))
    plt.pie(dt['number'], labels=dt['region'], autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    plt.title("Anzahl der Brände in den deutschen Bundesländern von 2000 bis 2024")
    plt.savefig('tortendiagramm.png')
    plt.close()
    
    # Zeitdiagramm speichern
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    
    fig, ax = plt.subplots(figsize=(12,8))
    for state, state_data in data.groupby('state'):
        ax.plot(state_data['year'], state_data['number'], label=state)
    ax.set_xlabel('Datum')
    ax.set_ylabel('Anzahl der Fälle')
    ax.set_title('Brände in deutschen Bundesländern von 2000 bis 2024')
    ax.legend()
    plt.savefig('zeitdiagramm.png')
    plt.close()

# Erstellung eines Berichts im PDF-Format
def create_report():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Bericht über die Anzahl der Brände in deutschen Bundesländern", ln = True, align = 'C')
    
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = "1. Anzahl der Brände in deutschen Bundesländern von 2000 bis 2024", ln = True)
    pdf.image("balkendiagramm.png", x = 10, y = 30, w = 180)
    
    pdf.add_page()
    pdf.cell(200, 10, txt = "2. Anzahl der Brände in den deutschen Bundesländern von 2000 bis 2024", ln = True)
    pdf.image("tortendiagramm.png", x = 10, y = 30, w = 180)
    
    pdf.add_page()
    pdf.cell(200, 10, txt = "3. Brände in deutschen Bundesländern von 2000 bis 2024", ln = True)
    pdf.image("zeitdiagramm.png", x = 10, y = 30, w = 180)
    
    pdf.output("Bericht_Braende_Deutschland.pdf")

# Hauptfunktion zum Ausführen aller Schritte
def main():
    df = pd.read_csv("./data2000_2024.csv")
    dt = pd.read_csv('./region.csv')
    data = pd.read_csv('./nrw.csv')
    
    df = clean_data(df)
    dt = clean_data(dt)
    data = clean_data(data)
    
    plot_bar_chart(df)
    plot_interactive_bar_chart(df)
    plot_pie_chart(dt)
    plot_interactive_pie_chart(dt)
    plot_time_series(data)
    plot_interactive_time_series(data)
    
    save_plots(df, dt, data)
    create_report()

if __name__ == "__main__":
    main()
