1. Meta Lead Testing Tool down - showing "Something went wrong" on 29 Aug. Used ReqBin with same payload structure as Meta (entry.changes.value.leadgen_id).
2. Used Firebase REST not SDK to keep Vercel light and avoid service-account.json.
3. Used custom /api/leads polling every 2 sec in Expo instead of direct SDK to keep Expo Go working without native modules.
4. Used documentId = leadId in PUT to avoid duplicate leads.
