import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl } from 'react-native';

const API_URL = 'https://unque-meta-leads-poc.vercel.app';

export default function App() {
  const [leads, setLeads] = useState([]);
  const [count, setCount] = useState(0);
  const [refreshing, setRefreshing] = useState(false);

  const fetchLeads = async () => {
    try {
      const res = await fetch(`${API_URL}/api/leads`);
      const data = await res.json();
      // Reverse to show newest first
      const reversed = (data.leads || []).slice().reverse();
      setLeads(reversed);
      setCount(data.count || 0);
    } catch (e) { 
      console.log(e); 
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchLeads();
    const interval = setInterval(fetchLeads, 2000); // Live update without touch
    return () => clearInterval(interval);
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchLeads();
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>UnQue - Live Meta Leads</Text>
      <Text style={styles.count}>Total: {count} | Auto-refresh 2s ⚡ LIVE</Text>
      
      <FlatList
        data={leads}
        keyExtractor={item => item.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        ListEmptyComponent={<Text style={styles.empty}>No leads yet. Submit test lead from Meta Tool...</Text>}
        renderItem={({ item, index }) => (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.name}>
                {item.field_data?.[0]?.values?.[0] || item.raw?.name?.stringValue || `Lead #${index+1}`}
              </Text>
              <Text style={styles.badge}>#{leads.length - index}</Text>
            </View>
            
            <Text style={styles.details}>
              {item.field_data 
                ? item.field_data.map(f => `${f.name}: ${f.values[0]}`).join('\n')
                : `name: ${item.raw?.name?.stringValue || 'Test User'} | phone: ${item.raw?.phone?.stringValue || '9999999999'}`
              }
            </Text>
            
            <Text style={styles.time}>ID: {item.id} | {new Date().toLocaleTimeString()}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, paddingTop: 60, backgroundColor: '#fff' },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 5 },
  count: { color: 'green', marginBottom: 15, fontWeight: 'bold', fontSize: 16 },
  empty: { textAlign: 'center', marginTop: 50, color: '#888' },
  card: { padding: 15, backgroundColor: '#f5f5f5', borderRadius: 12, marginBottom: 12, borderWidth: 1, borderColor: '#eee' },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  name: { fontWeight: 'bold', fontSize: 16 },
  badge: { backgroundColor: '#000', color: '#fff', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, fontSize: 10 },
  details: { fontSize: 13, lineHeight: 18 },
  time: { fontSize: 9, color: '#888', marginTop: 8 }
});
