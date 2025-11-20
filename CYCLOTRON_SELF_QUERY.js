/**
 * CYCLOTRON SELF-QUERY MODULE
 * Add this to any page to enable knowledge base searching
 *
 * Usage: Include this script, then call:
 *   cyclotronSearch('your query')
 *   cyclotronStats()
 */

const CYCLOTRON_INDEX_PATH = '.cyclotron_atoms/index.json';
let cyclotronIndex = null;

// Load index on page load
async function loadCyclotronIndex() {
    try {
        const response = await fetch(CYCLOTRON_INDEX_PATH);
        cyclotronIndex = await response.json();
        console.log(`⚛️ Cyclotron loaded: ${cyclotronIndex.total_atoms} atoms`);
        return true;
    } catch (e) {
        console.warn('Cyclotron index not available:', e);
        return false;
    }
}

// Search function
function cyclotronSearch(query, options = {}) {
    if (!cyclotronIndex) {
        console.warn('Cyclotron not loaded. Call loadCyclotronIndex() first.');
        return [];
    }

    const limit = options.limit || 20;
    const type = options.type || null;
    const queryLower = query.toLowerCase();

    let results = cyclotronIndex.atoms.filter(atom => {
        const nameMatch = atom.name.toLowerCase().includes(queryLower);
        const pathMatch = atom.path.toLowerCase().includes(queryLower);
        const typeMatch = !type || atom.type === type;
        return (nameMatch || pathMatch) && typeMatch;
    });

    // Sort by name match first
    results.sort((a, b) => {
        const aName = a.name.toLowerCase().includes(queryLower);
        const bName = b.name.toLowerCase().includes(queryLower);
        return bName - aName;
    });

    return results.slice(0, limit);
}

// Get stats
function cyclotronStats() {
    if (!cyclotronIndex) {
        return { error: 'Not loaded' };
    }

    return {
        total_atoms: cyclotronIndex.total_atoms,
        types: cyclotronIndex.atoms_by_type,
        last_updated: new Date(cyclotronIndex.last_updated * 1000).toLocaleString()
    };
}

// Quick search with console output
function cq(query) {
    const results = cyclotronSearch(query);
    console.log(`Found ${results.length} results for "${query}":`);
    results.forEach((r, i) => {
        console.log(`${i+1}. ${r.name} (${r.type}) - ${r.path}`);
    });
    return results;
}

// Auto-load on include
loadCyclotronIndex();

// Export for module use
if (typeof module !== 'undefined') {
    module.exports = { loadCyclotronIndex, cyclotronSearch, cyclotronStats, cq };
}
