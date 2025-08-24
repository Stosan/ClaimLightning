from datetime import datetime, timedelta
import random




def generate_mock_claims_list():
    """Generate list of mock claims"""
    statuses = ['processing','flagged', 'completed']
    names = ['Sam Ayo']
    claim_types = ['Motor Accident']
    
    claims = []
    num_claims = 1
    
    for i in range(num_claims):
        claim_id = "cl-123223"
        is_new = random.random() < 0.05  # 5% chance of being new
        
        claims.append({
            'id': claim_id,
            'claimantName': random.choice(names),
            'policyNumber': claim_id,
            'carRegistration': "2930-393",
            'status': 'pending' if is_new else random.choice(statuses),
            'claimType': random.choice(claim_types),
            'claimAmount': 1638.25,
            'dateSubmitted': (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
            'fraudScore': 0.0,
            'isNew': is_new,
            'lastUpdated': datetime.now().isoformat()
        })
    
    return claims

def generate_mock_claim_data(claim_id):
    """Generate realistic mock claim data"""
    names = ['Sam Ayo']
    claim_types = ['Motor Accident']
    
    base_data = {
        'id': claim_id,
        'claimantName': random.choice(names),
        'policyNumber': claim_id,
        'carRegistration': "2930-393",
        'status': random.choice(['approve']),
        'claimType': random.choice(claim_types),
        'claimDetails': 'Collision with reckless driver',
        'evidence': ['Photos', f'$1638.25 Invoice'],
        'claimAmount': 1638.25,
        'suggestedSettlement': 0,
        'fraudScore': 0,
        'confidenceScores': {
            'fraudDetection': 0,
            'repairCostEstimator': random.randint(80, 98),
            'documentVerification': random.randint(80, 90)
        },
        'missingFields': [],
        'aiRecommendations': [
            'Approve claim for expedited processing',
            'Confirm receipt of payment for repairs',
            'Validate pricing with certified garage',
            'Reach out to claimant to confirm acceptance'
        ],
        'timeline': [
            {
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                'action': 'submitted',
                'user': 'System'
            },
            {
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'action': 'ai_triage',
                'user': 'AI System'
            },
            {
                'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat(),
                'action': 'escalation_flagged',
                'user': 'AI System'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'action': 'under_review',
                'user': 'Admin User'
            }
        ],
        'dateSubmitted': (datetime.now() - timedelta(hours=2)).isoformat(),
        'lastUpdated': datetime.now().isoformat()
    }
    
    # Calculate suggested settlement (80-95% of claim amount)
    base_data['suggestedSettlement'] = int(base_data['claimAmount']) + (int(base_data['claimAmount']) * 0.05)
    
    return base_data