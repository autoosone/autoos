// Test the Blaxel API directly from browser console
// Copy and paste this into your browser console

(async () => {
    const API_KEY = 'bl_47yrrlxn6geic2wq9asrv5rapygyycj7';
    const ENDPOINT = 'https://run.blaxel.ai/amo/agents/template-copilot-kit-py';
    
    console.log('🚀 Testing Blaxel Agent...');
    
    try {
        const response = await fetch(ENDPOINT, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                inputs: 'Hello from browser console!'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('✅ SUCCESS! Response:', data);
            console.log('');
            console.log('🎉 THE API IS 100% WORKING!');
            console.log('');
            console.log('📝 To use in your app:');
            console.log('1. Open: http://localhost:8888/blaxel-test-interface.html');
            console.log('2. Or use the BlaxelAgent.jsx React component');
            console.log('3. Or copy this code into your application');
        } else {
            console.error('❌ Error:', data);
        }
    } catch (error) {
        console.error('❌ Exception:', error);
    }
})();
