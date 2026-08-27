import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl } from 'react-native';

const API_URL = 'https://unque-meta-leads-poc.vercel.app';

export default function App() {
  const [leads, setLeads] = useState([]);
  const [count, setCount] = useState(0);

  const fetchLeads = async () => {
    try {
      const res = await fetch(`${API_URL}/api/leads`);
      const data = await res.json();
      setLeads(data.leads || []);
      setCount(data.count || 0);
    } catch (e) { console.log(e) }
  };

  useEffect(() => {
    fetchLeads();
    const interval = setInterval(fetchLeads, 2000); // Live update without touch
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.header}>UnQue - Live Meta Leads</Text>
      <Text style={styles.count}>Total: {count} | Auto-refresh 2s</Text>
      <FlatList
        data={leads}
        keyExtractor={item => item.id}
        refreshControl={<RefreshControl refreshing={false} onRefresh={fetchLeads} />}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.field_data[0]?.values[0]}</Text>
            <Text>{item.field_data.map(f => `${f.name}: ${f.values[0]}`).join(' | ')}</Text>
            <Text style={styles.time}>{item.created_time}</Text>
          </View>
        )}
      />
    </View>
  );
}
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, paddingTop: 50, backgroundColor: '#fff' },
  header: { fontSize: 22, fontWeight: 'bold', marginBottom: 10 },
  count: { color: 'green', marginBottom: 15, fontWeight: 'bold' },
  card: { padding: 15, backgroundColor: '#f5f5f5', borderRadius: 10, marginBottom: 10 },
  name: { fontWeight: 'bold', fontSize: 16 },
  time: { fontSize: 10, color: '#888', marginTop: 5 }
});
