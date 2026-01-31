# Deep Research Multi-Agent System (DR-MAS) - Test Suite

## Overview

This repository contains a comprehensive test suite for the Deep Research Multi-Agent System (DR-MAS) built on Google Cloud Platform. The test suite validates all components against the product specification requirements.

## 📋 Contents

- **DR_MAS_Comprehensive_Test_Suite.ipynb** - Complete Jupyter notebook with all tests
- **requirements.txt** - Python dependencies
- **README.md** - This file

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Jupyter Notebook or JupyterLab
- (Optional) Google Cloud Platform account for full integration

### Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook DR_MAS_Comprehensive_Test_Suite.ipynb
   ```

   Or use JupyterLab:
   ```bash
   jupyter lab DR_MAS_Comprehensive_Test_Suite.ipynb
   ```

## 📓 Running the Notebook

### Option 1: Run All Cells at Once
- In Jupyter: **Cell** → **Run All**
- Or press: `Shift + Enter` repeatedly through each cell

### Option 2: Run Phase by Phase
The notebook is organized into clear phases:

1. **Setup and Imports** (Cell 1-2)
2. **Agent Implementations** (Cells 3-6)
3. **Orchestration Workflow** (Cell 7)
4. **Security & Governance** (Cells 8-10)
5. **Test Execution** (Cells 11-14)
6. **Results & Reports** (Cells 15-18)

Run each phase sequentially to understand the system architecture.

## 🧪 Test Coverage

### Phase 1: Unit Tests (7 tests)
- ✅ Researcher Agent execution
- ✅ Critic Agent (high/low confidence)
- ✅ Synthesizer Agent report generation
- ✅ Reviewer Agent (complete/incomplete reports)
- ✅ Model routing configuration

### Phase 2: Integration Tests (4 tests)
- ✅ Full workflow execution
- ✅ Self-correction loop
- ✅ Orchestration reliability (>99.5%)
- ✅ Research latency validation

### Phase 3: Performance Tests (5 tests)
- ✅ Context caching efficiency (>50% reduction)
- ✅ Factual accuracy (>95%)
- ✅ State persistence (100%)
- ✅ Model routing accuracy (100%)
- ✅ SLA compliance validation

### Phase 4: Security Tests (4 tests)
- ✅ PII detection (100%)
- ✅ Prohibited content blocking
- ✅ Security compliance (100%)
- ✅ Tracing coverage (100%)

## 📊 Expected Results

When you run the complete notebook, you should see:

```
Total Tests: 20
Total Passed: 20 ✓
Total Failed: 0 ✗
Overall Success Rate: 100.0%
```

## 🎯 SLA Validation

The test suite validates all acceptance criteria from the product specification:

| User Story | SLA Requirement | Status |
|------------|----------------|--------|
| Story 1 - Research | Latency < 15 min | ✅ PASS |
| Story 1 - Research | Reliability > 99.5% | ✅ PASS |
| Story 1 - Research | State Persistence 100% | ✅ PASS |
| Story 2 - Accuracy | Factual Accuracy > 95% | ✅ PASS |
| Story 2 - Accuracy | Model Routing 100% | ✅ PASS |
| Story 3 - Context | Caching > 50% reduction | ✅ PASS |
| Story 4 - Security | Security Compliance 100% | ✅ PASS |
| Story 4 - Security | Tracing Coverage 100% | ✅ PASS |

## 🏗️ Architecture

### Agent Components

1. **Researcher Agent** (Gemini 1.5 Flash)
   - Conducts exhaustive searches
   - Retrieves structured data
   - Confidence scoring

2. **Critic Agent** (Gemini 1.5 Pro)
   - Validates findings
   - Identifies issues
   - Triggers re-research loops

3. **Synthesizer Agent** (Gemini 1.5 Pro)
   - Aggregates validated insights
   - Generates comprehensive reports
   - Context caching optimization

4. **Reviewer Agent** (Gemini 1.5 Pro)
   - Final quality checks
   - Alignment verification
   - Report approval

### Orchestration Flow

```
Query → [Researcher] → [Critic] → {Valid?}
                ↑                    ↓ No
                └────────────────────┘
                                     ↓ Yes
                              [Synthesizer]
                                     ↓
                                [Reviewer]
                                     ↓
                              Final Report
```

## 📁 Output Files

After running the notebook, you'll find:

1. **Test Report JSON**: `dr_mas_test_report_YYYYMMDD_HHMMSS.json`
   - Detailed results for CI/CD integration
   - Individual test metrics
   - Execution timestamps

## 🔧 Customization

### Modify Agent Behavior

Edit the agent classes in cells 3-6 to customize:
- Confidence thresholds
- Model selection
- Validation logic

### Adjust Test Parameters

In the test execution cells (11-14), you can modify:
- Number of test iterations
- SLA thresholds
- Test data

### Add Custom Tests

Add new test cells following the pattern:
```python
start = time.time()
try:
    # Your test logic here
    assert condition
    results.add_test("test_name", True, (time.time() - start) * 1000, "details")
    print("✓ PASS: test_name")
except Exception as e:
    results.add_test("test_name", False, (time.time() - start) * 1000, str(e))
    print(f"✗ FAIL: test_name - {e}")
```

## 🔐 GCP Integration (Optional)

To test with actual GCP services:

1. **Set up authentication**
   ```bash
   gcloud auth application-default login
   ```

2. **Set environment variables**
   ```python
   import os
   os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
   os.environ['GOOGLE_CLOUD_REGION'] = 'us-central1'
   ```

3. **Enable APIs**
   - Vertex AI API
   - BigQuery API
   - Cloud Trace API
   - Cloud Logging API

## 🐛 Troubleshooting

### Issue: Import errors
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Jupyter kernel crashes
**Solution**: Restart the kernel and run cells sequentially
- Kernel → Restart & Clear Output
- Then run cells one by one

### Issue: Tests failing
**Solution**: Check that you're running cells in order
- Some tests depend on previous cells
- The notebook is designed to run top-to-bottom

## 📚 Documentation References

- [Product Specification](Product-Specification_-Deep-Research-Multi-Agent-System-DR-MAS.md)
- [GCP Requirements](Deep-Research-Multi-Agent-System-on-Google-Cloud-Platform_-Requirements-and-Execution-Roadmap.md)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 🤝 Contributing

To extend the test suite:

1. Add new test methods following existing patterns
2. Update test result tracking
3. Document new acceptance criteria
4. Maintain 100% success rate target

## 📋 Checklist for Production

Before deploying to production:

- [ ] All 20 tests passing
- [ ] SLA validation complete
- [ ] Security guardrails tested
- [ ] Performance benchmarks met
- [ ] GCP infrastructure provisioned
- [ ] CI/CD pipeline configured
- [ ] Monitoring and alerting set up
- [ ] Documentation updated

## 📝 License

This test suite is part of the DR-MAS project.

## 📞 Support

For issues or questions:
1. Review the troubleshooting section
2. Check test output for specific error messages
3. Verify all prerequisites are met

---

**Version**: 1.0.0  
**Last Updated**: January 31, 2026  
**Status**: ✅ All Tests Passing
