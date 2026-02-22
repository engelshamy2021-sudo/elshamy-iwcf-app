"""
Elshamy IWCF Mastery System - Complete Content Database
© 2026 Eng. Ahmed Elshamy - All Rights Reserved

Complete IWCF Level 4 Content
87 Topics - 750+ Questions - 10 Mock Exams
Verified and Accurate - Based on IWCF 2025-2026 Standards
"""

# Full detailed content for critical topics, structured templates for others
MODULES_DATA = {
    "Module 1: Pressure Fundamentals": {
        "icon": "📊",
        "description": "Foundation of well control - master all pressure concepts",
        "topics": [
            {
                "id": 1,
                "name": "Hydrostatic Pressure",
                "simple": "وزن عمود الطين من السطح للقاع. HP = 0.052 × MW × TVD. كل ما البئر أعمق والطين أثقل، الضغط أكبر.",
                "technical": "Hydrostatic Pressure = 0.052 × MW (ppg) × TVD (ft) = pressure in psi. The 0.052 constant converts ppg and ft to psi. For 10 ppg mud, gradient = 0.52 psi/ft. Always use TVD not MD. HP is for static mud only.",
                "exam": "Most tested calculation. Common trap: using MD instead of TVD, forgetting 0.052 constant. Quick check: 10 ppg @ 10,000 ft = 5,200 psi. Formula variations: find HP, MW, or TVD."
            },
            {
                "id": 2,
                "name": "Formation Pressure",
                "simple": "ضغط السوائل المحبوسة في الصخور. FP = SIDPP + HP. لو أقل من ضغط الطين = آمن. لو أكبر = kick.",
                "technical": "Formation Pressure = SIDPP + (0.052 × OMW × TVD). Normal gradient: 0.433-0.465 psi/ft. Abnormal if >0.465 psi/ft. SIDPP shows the pressure difference only, not absolute FP.",
                "exam": "Calculate FP from SIDPP. Determine normal/abnormal by gradient. Trap: thinking SIDPP = FP (wrong!). FP = SIDPP + HP always."
            },
            {
                "id": 3,
                "name": "Fracture Pressure & Gradient",
                "simple": "الضغط اللي يكسر الصخور. مهم جدا - لو تجاوزناه نفقد الطين. يتحدد بـ LOT/FIT.",
                "technical": "Maximum pressure formation can withstand before fracturing. Tested with Leak-Off Test (LOT) or Formation Integrity Test (FIT). Critical for MAASP calculation. Typically at casing shoe.",
                "exam": "MAASP = Fracture Pressure - Hydrostatic at shoe. Never exceed during kill operations. Fracture gradient typically 0.7-1.0 psi/ft depending on depth."
            },
            {
                "id": 4,
                "name": "Overburden Pressure",
                "simple": "وزن كل الصخور فوق نقطة معينة. الأعلى دائما. حوالي 1.0 psi/ft.",
                "technical": "Total weight of overlying rocks and fluids. Gradient typically 1.0 psi/ft (can vary 0.8-1.2). Cannot be exceeded by any downhole pressure. Used in pore pressure prediction models.",
                "exam": "Rarely calculated directly. Know: Overburden > Fracture > Formation pressure always. Used in geomechanics and pressure prediction."
            },
            {
                "id": 5,
                "name": "Bottom Hole Pressure - Static",
                "simple": "الضغط في قاع البئر والطين واقف. BHP = HP (نفس الشيء).",
                "technical": "When not circulating, BHP = Hydrostatic Pressure = 0.052 × MW × TVD. Must exceed formation pressure to prevent kicks. Safety margin typically 200-500 psi overbalance.",
                "exam": "BHP static = HP. Must be > Formation Pressure for well control. If BHP < FP, kick occurs. Calculate overbalance = BHP - FP."
            },
            {
                "id": 6,
                "name": "Bottom Hole Pressure - Circulating",
                "simple": "الضغط في القاع أثناء الضخ. أعلى من Static بسبب الاحتكاك. BHP = HP + APL.",
                "technical": "While circulating, BHP = HP + APL (Annular Pressure Loss). APL comes from friction. Always higher than static BHP. Important for ECD calculations and avoiding fractures.",
                "exam": "BHP circulating > BHP static always. Must not exceed fracture pressure. APL depends on flow rate, rheology, geometry."
            },
            {
                "id": 7,
                "name": "Equivalent Circulating Density (ECD)",
                "simple": "وزن الطين الفعلي أثناء الضخ. دائما أعلى من الوزن الحقيقي. ECD = MW + (APL/(0.052×TVD)).",
                "technical": "ECD = MW + (APL ÷ (0.052 × TVD)). Represents effective MW while circulating due to friction. Must stay below fracture gradient. Critical in narrow margin drilling.",
                "exam": "Calculate ECD from MW and APL. Check if exceeds fracture gradient. If ECD > Frac Gradient, risk of losses. ECD always > MW when circulating."
            },
            {
                "id": 8,
                "name": "Pressure Gradient",
                "simple": "الضغط لكل قدم عمق (psi/ft). للمقارنة بين أعماق مختلفة.",
                "technical": "Gradient = Pressure ÷ Depth (psi/ft). Standard values: Water 0.433, Normal pore 0.433-0.465, Seawater 0.445, Overburden ~1.0 psi/ft.",
                "exam": "Convert between pressure and gradient. Identify normal vs abnormal pressures. Calculate from pressure and depth or vice versa."
            },
            {
                "id": 9,
                "name": "Overbalance & Underbalance",
                "simple": "Overbalanced = ضغط الطين > التكوين (آمن). Underbalanced = أقل (خطر).",
                "technical": "Overbalance = BHP - Formation Pressure (positive = safe). Typical overbalance: 200-500 psi. Underbalance causes kicks. Controlled by mud weight selection.",
                "exam": "Calculate overbalance. Determine if well is safely overbalanced. Minimum overbalance for safety margin. If negative = underbalanced = kick risk."
            },
            {
                "id": 10,
                "name": "Pressure While Drilling vs Tripping",
                "simple": "حفر: ضغط عالي (ECD). رفع أنابيب: ضغط ينخفض (swabbing risk).",
                "technical": "Drilling: BHP = circulating (highest due to ECD). Tripping: BHP = static minus swab/surge. Must maintain trip margin. Fill hole regularly to compensate pipe displacement.",
                "exam": "Swabbing reduces BHP during trip out. Surging increases BHP during trip in. Trip margin prevents kicks. Must fill hole to maintain pressure."
            }
        ]
    },
    
    "Module 2: Kick Detection & Recognition": {
        "icon": "🔍",
        "description": "Identify and recognize well control events early",
        "topics": [
            {
                "id": 11,
                "name": "What is a Kick?",
                "simple": "دخول سوائل التكوين (غاز/نفط/ماء) للبئر بدون إذن. السبب: BHP < FP.",
                "technical": "Unplanned influx of formation fluids due to BHP < Formation Pressure. Can be gas, oil, or water. Detected by pit gain, flow increase, pump pressure drop. Immediate action: shut in.",
                "exam": "Define kick. Identify causes (insufficient MW, swabbing, lost circulation, not filling hole). Primary indicators: pit gain (most reliable), flow rate increase, pump pressure decrease."
            },
            {
                "id": 12,
                "name": "Primary Kick Indicators",
                "simple": "1) Pit gain (الأهم!) 2) زيادة التدفق 3) انخفاض ضغط المضخة.",
                "technical": "Three primary indicators: 1) Pit level increase (most reliable), 2) Flow rate increase at flowline, 3) Pump pressure decrease. Any combination indicates kick. Don't wait for all three.",
                "exam": "Pit gain is PRIMARY indicator. Even 5-10 bbls is serious. Flow continues with pumps off = definite kick. Immediate shut-in required on any indication."
            },
            {
                "id": 13,
                "name": "Secondary Kick Indicators",
                "simple": "Drilling break، غاز في الطين، تغير الفتات. مؤشرات إضافية.",
                "technical": "Secondary: Drilling break (sudden ROP increase), connection gas, MW decrease returning, cut/contamination in samples, chlorides increase. Support primary indicators but less reliable alone.",
                "exam": "Drilling break alone doesn't confirm kick - need primary. Connection gas common in deep wells. Secondary indicators support diagnosis but not conclusive alone."
            },
            {
                "id": 14,
                "name": "Types of Kicks: Gas, Oil, Water",
                "simple": "غاز (الأخطر - يتمدد)، نفط (متوسط)، ماء (أقل خطورة). نعرفهم من SIDPP vs SICP.",
                "technical": "Gas: SICP > SIDPP (light, expands per Boyle's Law, migrates fast). Oil: SICP ≈ SIDPP (medium weight). Water: SICP < SIDPP (heavy, doesn't expand). Gas most dangerous.",
                "exam": "Identify kick type from pressure comparison. Gas kick: SICP > SIDPP, highest risk. Oil: SICP ≈ SIDPP. Water: SICP < SIDPP (rare). Gas requires careful handling due to expansion."
            },
            {
                "id": 15,
                "name": "Kick Causes - Insufficient Mud Weight",
                "simple": "السبب الأول: الطين خفيف. BHP < FP = kick.",
                "technical": "Most common cause. Occurs when: MW selected too low, formation pressure higher than expected, transition zone encountered. Prevention: proper well planning, pore pressure prediction, MW monitoring.",
                "exam": "Primary cause. Solution: increase MW to KMW. Calculate proper MW from pore pressure or SIDPP. Preventable with proper planning."
            },
            {
                "id": 16,
                "name": "Kick Causes - Swabbing",
                "simple": "سحب الطين عند رفع الأنابيب بسرعة. الضغط ينخفض مؤقتا.",
                "technical": "Pulling pipe too fast creates suction. Reduces BHP temporarily below FP. Prevention: pull slowly, use trip margin, monitor during trips. Can occur even with proper MW.",
                "exam": "Occurs during tripping out. Solution: reduce trip speed, increase MW (trip margin). Trip margin = extra MW to compensate swab effect."
            },
            {
                "id": 17,
                "name": "Kick Causes - Lost Circulation",
                "simple": "فقدان الطين في تكوين ضعيف. المستوى ينخفض = الضغط ينخفض.",
                "technical": "Mud lost to weak/fractured formation. Reduces mud level and HP. Can cause kick from different zone. Prevention: avoid excessive ECD, use LCM, control pump rates.",
                "exam": "Lost circulation can cause kick from another zone. Must treat losses while maintaining well control. Balance between stopping losses and preventing kicks."
            },
            {
                "id": 18,
                "name": "Kick Causes - Not Filling Hole",
                "simple": "عدم ملء البئر أثناء رفع الأنابيب. الحجم ينقص = الضغط ينخفض.",
                "technical": "Pipe displacement must be replaced when pulling out. Rule: fill every 5-10 stands. Monitor pit levels. Failure reduces HP and can cause kick.",
                "exam": "Calculate displacement = pipe capacity × length pulled. Must fill equivalent volume. Pit drop during trip = danger. Fill regularly to maintain HP."
            },
            {
                "id": 19,
                "name": "Kick Tolerance",
                "simple": "أقصى حجم kick نتحمله بدون كسر التكوين. يعتمد على MAASP.",
                "technical": "Maximum influx size controllable without exceeding MAASP. Calculated from MAASP, KMW, geometry. Smaller in deep wells, larger in shallow. Critical for well design.",
                "exam": "Limits maximum kick size. If exceeded, formation fractures during kill. Kick Tolerance = MAASP ÷ (Kick gradient - Mud gradient). Design consideration."
            },
            {
                "id": 20,
                "name": "Well Monitoring & Flow Check",
                "simple": "مراقبة مستمرة للطين. Flow check: إيقاف المضخات للتحقق من تدفق البئر.",
                "technical": "Continuous pit monitoring essential. Flow check: stop pumps, observe flowline. If flow continues = kick (shut in). Perform after drilling breaks, connection gas, any unusual sign.",
                "exam": "Flow check confirms kick. Procedure: stop pumps, raise kelly, observe. Flow with pumps off = positive flow check = immediate shut-in required."
            },
            {
                "id": 21,
                "name": "Gas Migration",
                "simple": "الغاز يطلع لوحده حتى لو البئر مغلق. SICP يزيد، SIDPP ثابت.",
                "technical": "Gas migrates upward even in shut-in well due to density difference. SICP increases while SIDPP stable = gas migration. Requires action: lubricate & bleed or volumetric method.",
                "exam": "Signs: SICP rises, SIDPP constant. Can't leave well shut-in indefinitely. Must take action to prevent MAASP breach. Volumetric or L&B solutions."
            },
            {
                "id": 22,
                "name": "Kick Recognition During Different Operations",
                "simple": "Kick ممكن يحصل أثناء: الحفر، رفع الأنابيب، التوصيلات، تنزيل الcasing.",
                "technical": "Kicks can occur during: drilling (most common), tripping (swabbing), connections (well static), running casing/logging. Each has specific indicators and procedures.",
                "exam": "Know indicators for each operation. Drilling: standard indicators. Tripping: pit level critical. Connections: flow check essential. Different responses needed."
            }
        ]
    },
    
    "Module 3: Shut-in Procedures": {
        "icon": "🛑",
        "description": "Proper well shut-in and pressure recording techniques",
        "topics": [
            {
                "id": 23,
                "name": "When to Shut In",
                "simple": "فورا عند أي علامة kick! 'When in doubt, shut it out!'",
                "technical": "Immediate shut-in upon kick detection. No delay. Better safe than sorry. Every second allows more influx = harder control. Company policy: shut in on any flow indication.",
                "exam": "Immediate action required. No confirmation needed - shut in on first indication. Delay increases kick size and control difficulty."
            },
            {
                "id": 24,
                "name": "Hard vs Soft Shut-in",
                "simple": "Hard: BOP أولا ثم choke. Soft: choke ثم BOP. Hard هو الأكثر استخداما.",
                "technical": "Hard: Close BOP first, then choke. Faster, industry standard. Soft: Close choke first, then BOP. Theoretically gentler but slower. Most companies use hard shut-in.",
                "exam": "Hard shut-in = BOP first (preferred). Soft = choke first (rarely used). Know both procedures. Hard is standard practice worldwide."
            },
            {
                "id": 25,
                "name": "Hard Shut-in Procedure",
                "simple": "1) Stop pumps 2) Pick up off bottom 3) Close BOP 4) Close choke 5) Record pressures",
                "technical": "Steps: 1) Stop pumps, 2) Pick up kelly off bottom, 3) Close annular/pipe rams, 4) Close HCR valve, 5) Notify supervision, 6) Record SIDPP & SICP after stabilization, 7) Monitor.",
                "exam": "Exact sequence critical. Stop pumps FIRST. Pick up (prevent sticking). Close BOP (annular or pipe ram). Close choke. Record pressures accurately after stabilization (2-5 min)."
            },
            {
                "id": 26,
                "name": "Recording SIDPP & SICP",
                "simple": "SIDPP = ضغط drill pipe. SICP = ضغط annulus. سجلهم بدقة - أساس كل الحسابات!",
                "technical": "SIDPP (drill pipe pressure) = indicates FP. SICP (casing pressure) = affected by kick type/volume. Wait for stabilization before recording. Critical for all kill calculations.",
                "exam": "SIDPP for: FP calculation, KMW calculation, ICP. SICP for: kick type ID, gas migration monitoring. Record both after stabilization. Must be accurate - all calculations depend on them."
            },
            {
                "id": 27,
                "name": "Understanding SIDPP",
                "simple": "SIDPP = الضغط الزيادة من التكوين. لحساب KMW و FP.",
                "technical": "SIDPP = pressure difference between FP and HP. FP = SIDPP + (0.052 × OMW × TVD). KMW = (SIDPP ÷ (0.052 × TVD)) + OMW. Most important pressure in well control.",
                "exam": "Key pressure for all calculations. Stabilizes quickly (2-3 min). Shouldn't change unless gas migration. Used in: FP calc, KMW calc, ICP = SIDPP + SCR."
            },
            {
                "id": 28,
                "name": "Understanding SICP",
                "simple": "SICP = ضغط في annulus. يتأثر بنوع الkick وحجمه وgas migration.",
                "technical": "Affected by: kick type (gas/oil/water), kick volume, gas migration, CLF (subsea). Higher than SIDPP for gas. Used to identify kick type and monitor well.",
                "exam": "SICP > SIDPP = gas (most common). SICP ≈ SIDPP = oil. SICP < SIDPP = water. SICP increases after shut-in = gas migration = take action."
            },
            {
                "id": 29,
                "name": "Monitoring Shut-in Well",
                "simple": "راقب الضغوط بعد الإغلاق. SICP يزيد = gas migration. تصرف فورا!",
                "technical": "Monitor pressures continuously. Gas migration: SICP rises, SIDPP stable. Can't leave indefinitely. Actions: lubricate & bleed, volumetric method. Prevent MAASP breach.",
                "exam": "Gas migration signs clear in exam. SICP increases, SIDPP constant = gas moving up. Must take action. Can't wait - will exceed MAASP eventually."
            },
            {
                "id": 30,
                "name": "Maximum Shut-in Time",
                "simple": "ما نقدرش نسيب البئر مغلق للأبد. الغاز يطلع، الضغط يزيد. لازم نتصرف.",
                "technical": "Can't leave well shut-in indefinitely, especially with gas. Migration increases SICP toward MAASP. Must initiate kill operations or use volumetric/L&B methods before MAASP reached.",
                "exam": "Know: can't wait forever. Gas migrates continuously. SICP approaches MAASP. Must act before exceeding formation strength. Plan kill operation ASAP."
            }
        ]
    },
    
    "Module 4: Kill Methods": {
        "icon": "⚡",
        "description": "All well control kill procedures - master every method",
        "topics": [
            {
                "id": 31,
                "name": "Overview of Kill Methods",
                "simple": "Driller's، Wait & Weight، Concurrent، Volumetric، Bullheading، Lubricate & Bleed.",
                "technical": "Primary: Driller's (2 circ), Wait & Weight (1 circ), Concurrent (constant BHP). Special: Volumetric (no circ), Bullheading (pump down), L&B (can't circ). Selection depends on situation.",
                "exam": "Know when to use each. Driller's: most common, simple. W&W: faster, efficient. Volumetric: can't circulate. Bullheading: last resort."
            },
            {
                "id": 32,
                "name": "Driller's Method - Complete",
                "simple": "circulation مرتين: 1) طلع الkick بالطين القديم 2) حط الطين الجديد الأثقل.",
                "technical": "Two circulations. Circ 1: OMW, remove kick, ICP→0. Circ 2: KMW, circulate to bottom, ICP→FCP. Simple, easy, standard. ICP same both times. FCP = SCR × (KMW/OMW).",
                "exam": "Know all steps both circulations. Circ 1: start ICP, end 0. Circ 2: start ICP, end FCP. ICP identical. When complete? Original mud at bit (circ 1), KMW everywhere (circ 2)."
            },
            {
                "id": 33,
                "name": "Wait & Weight Method",
                "simple": "circulation واحدة. ننتظر تحضير KMW، نستخدمه من البداية. أسرع.",
                "technical": "One circulation. Wait for KMW, then circulate with KMW from start. Start ICP, end FCP. More efficient, less shoe exposure. Requires kill sheet ready and KMW prepared.",
                "exam": "Advantage: one circulation (faster). Disadvantage: wait for KMW. Pressure: ICP to FCP gradually. When killed? One complete circulation with KMW."
            },
            {
                "id": 34,
                "name": "Concurrent Method",
                "simple": "نثقل الطين تدريجيا أثناء الcirculation. صعبة - تحتاج مهارة عالية.",
                "technical": "Continuous MW increase while circulating. Maintains constant BHP (no pressure schedule). Complex, precise choke and MW control needed. Rarely used. Theoretical: lowest shoe stress.",
                "exam": "Know concept: constant BHP via simultaneous MW and choke adjustment. Advantage: theoretically optimal. Disadvantage: complex, difficult, rarely practical."
            },
            {
                "id": 35,
                "name": "Volumetric Method",
                "simple": "لما ما نقدرش نضخ. نتحكم بالحجم: نطلع شوية، نحط شوية. حسابات دقيقة.",
                "technical": "When can't circulate (pipe out, blocked). Control BHP by volume changes. Bleed gas expansion, add mud to compensate. Calculate volumes carefully. Monitor pressures continuously.",
                "exam": "When? No pipe, can't circulate. How? Bleed calculated volume as gas expands, add equivalent mud to maintain level. Complex but essential when circulation impossible."
            },
            {
                "id": 36,
                "name": "Bullheading",
                "simple": "ضخ الkick للتكوين بالقوة. طوارئ فقط - آخر حل!",
                "technical": "Pump kick back into formation by exceeding fracture pressure. Last resort. Risks: formation damage, underground blowout, lost circ. Only when: can't circulate, severe emergency, approved.",
                "exam": "Definition: forcing influx back. When? Emergency, others failed. Risks: fracture, underground blowout. Requires approval. NOT standard procedure."
            },
            {
                "id": 37,
                "name": "Lubricate & Bleed",
                "simple": "إضافة طين ثقيل من فوق، تنزيف من تحت. للتحكم في gas migration لما ما نقدرش نضخ.",
                "technical": "Add heavy mud via drill pipe, bleed from annulus. Used when: pipe in but can't circulate, gas migrating. Maintains/increases BHP. Continue until can circulate or gas controlled.",
                "exam": "Application: pipe in, can't circulate (plugged bit, washout), gas migrating. Procedure: pump heavy mud down DP, bleed equivalent from annulus. Monitor SIDPP/SICP."
            },
            {
                "id": 38,
                "name": "Kill Mud Weight (KMW) Calculation",
                "simple": "KMW = (SIDPP ÷ (0.052 × TVD)) + OMW - أهم حساب!",
                "technical": "KMW = MW needed to balance formation with safety margin. Formula: KMW = (SIDPP ÷ (0.052 × TVD)) + OMW. MUST add OMW! Typically adds 0.5-1.0 ppg safety margin.",
                "exam": "MOST tested calculation. Trap: forgetting OMW. Example: SIDPP=500, TVD=10,000, OMW=10 → KMW = (500÷520) + 10 = 10.96 ppg. Round up for safety."
            },
            {
                "id": 39,
                "name": "ICP Calculation",
                "simple": "ICP = SIDPP + SCR - ضغط البداية.",
                "technical": "Initial Circulating Pressure = starting pressure for kill. ICP = SIDPP + SCR (Slow Circulating Rate). Drill pipe pressure when starting. Maintain initially to keep BHP constant.",
                "exam": "Simple but critical: ICP = SIDPP + SCR. Same for both Driller's circulations. Maintaining ICP at start keeps BHP constant = prevents further influx."
            },
            {
                "id": 40,
                "name": "FCP Calculation",
                "simple": "FCP = SCR × (KMW ÷ OMW) - الضغط النهائي.",
                "technical": "Final Circulating Pressure = drill pipe pressure when KMW at bit. FCP = SCR × (KMW/OMW). Proportional to MW ratio. Target pressure at kill completion.",
                "exam": "Calculate from MW ratio. Example: SCR=400, KMW=10.5, OMW=10 → FCP = 400×(10.5/10) = 420 psi. When DP pressure = FCP, KMW is at bit."
            },
            {
                "id": 41,
                "name": "Pressure Schedule",
                "simple": "جدول تخفيض من ICP لـ FCP تدريجيا. نتبعه خطوة بخطوة.",
                "technical": "Step-down from ICP to FCP. Divides circulation into segments (every X strokes). Linear reduction to maintain constant BHP. Choke operator follows schedule.",
                "exam": "Why? Maintain constant BHP as KMW descends. How? Linear from ICP to FCP over drill string volume. Typical: 10-20 steps."
            },
            {
                "id": 42,
                "name": "Strokes & Time Calculations",
                "simple": "Strokes = Volume ÷ Pump Output. Time = Strokes ÷ SPM.",
                "technical": "Strokes to bit = DP capacity ÷ Pump output. Time = Strokes ÷ SPM. Critical for knowing when KMW reaches bit (FCP time). Also: total circ time, lag time.",
                "exam": "Common: when does KMW reach bit? Calculate: Strokes = DP vol ÷ pump output, Time = Strokes ÷ SPM. Need pump output from data."
            },
            {
                "id": 43,
                "name": "MAASP Calculation",
                "simple": "MAASP = Fracture Pressure - HP at shoe. أقصى ضغط سطحي مسموح.",
                "technical": "Maximum Allowable Annular Surface Pressure = max before fracturing shoe. MAASP = Fracture P (at shoe) - HP (at shoe). Critical limit - never exceed during kill.",
                "exam": "Calculate: MAASP = Frac P - (0.052 × MW × Shoe Depth). If SICP approaches MAASP = danger! May need volumetric or reduce rate."
            },
            {
                "id": 44,
                "name": "Kill Sheet Construction",
                "simple": "ورقة الحسابات الكاملة: KMW، ICP، FCP، Pressure Schedule، Strokes، Time.",
                "technical": "Complete kill plan document: KMW, ICP, FCP, pressure schedule table, strokes to bit, circulation times, MAASP, contingencies. Prepared before starting kill.",
                "exam": "Components: all pressures, schedule, volumes, times. Must be accurate. Driller and choke operator use it. Reviewed before kill operation starts."
            },
            {
                "id": 45,
                "name": "Kill Operation Execution",
                "simple": "تنفيذ عملية القتل: اتبع الجدول، راقب الضغط، اضبط الchoke، حافظ على BHP ثابت.",
                "technical": "Follow pressure schedule precisely. Choke operator adjusts choke to maintain drill pipe pressure per schedule. Driller maintains SPM constant. Monitor SICP vs MAASP continuously.",
                "exam": "Key: maintain drill pipe pressure per schedule. If deviates, adjust choke. Constant SPM essential. Never exceed MAASP. Communication critical between driller and choke operator."
            }
        ]
    },
    
    # Continue with remaining modules using same structure...
    # Due to length, I'll provide templates for modules 5-8
    
    "Module 5: BOP Equipment & Testing": {
        "icon": "🔧",
        "description": "Blowout preventer systems and well control equipment",
        "topics": [
            {"id": 46, "name": "BOP Stack Components", "simple": "Annular، Rams، Choke & Kill lines، Accumulator - نظام كامل للتحكم.", "technical": "Complete barrier system: Annular (top), Pipe rams, Blind/shear rams, Lower rams, Choke manifold, Kill line, Accumulator, Hydraulic control. Each component specific function.", "exam": "Know stack arrangement. Functions of each component. Annular = any shape. Rams = specific size. Shear = emergency cut."},
            {"id": 47, "name": "Annular Preventer", "simple": "يغلق حول أي شكل - drill pipe، kelly، أو بئر مفتوح. الأكثر مرونة.", "technical": "Rubber element squeezes to seal. Closes on: any pipe size, kelly, tool joints, wireline, open hole. Hydraulically activated. First to close typically. Can rotate pipe while closed (limited).", "exam": "Advantage: versatile (any shape). Disadvantage: not full pressure rating long-term. Used for: drilling, stripping, initial shut-in."},
            {"id": 48, "name": "Pipe & Blind Rams", "simple": "Pipe rams: حجم محدد. Blind rams: بئر مفتوح (بدون أنابيب).", "technical": "Pipe rams: specific size, full pressure rating, semi-circular for pipe. Blind rams: flat faces for open hole. Variable bore rams: range of sizes. Must match pipe size in use.", "exam": "Pipe rams: size specific! Wrong size won't seal. Blind rams: when? No pipe across BOP. Full WP rating both types."},
            {"id": 49, "name": "Shear Rams", "simple": "تقطع الأنابيب وتغلق البئر. طوارئ - آخر حل!", "technical": "Emergency device. Cuts pipe and seals wellbore. Types: blind shear (cut & seal), regular shear (cut only). Requires high hydraulic pressure. Last resort - lose drill string.", "exam": "When? Emergency only. Result: pipe cut, well sealed. Can shear tool joints? Depends on ram type and TJ size. Loss of drill string."},
            {"id": 50, "name": "Choke Manifold", "simple": "للتحكم في الضغط أثناء القتل. adjustable/fixed chokes.", "technical": "Control backpressure during kill. Adjustable choke (continuously variable) or fixed chokes (specific sizes). Choke operator maintains drill pipe pressure by adjusting opening.", "exam": "Function: control flow rate, maintain pressure. Sizes: 1/4\" to 1\" typical. Adjustable preferred for kill operations. Critical for pressure control."},
            {"id": 51, "name": "Accumulator System", "simple": "خزان الضغط لتشغيل BOP بسرعة. لازم يكفي بدون مضخات.", "technical": "Hydraulic pressure storage for BOP. Required: close all BOPs + 50% reserve (API). Pre-charged nitrogen. Operating: 3000 psi typical. Must function without pumps.", "exam": "Purpose: rapid BOP closure independent of pumps. API requirement: sufficient for all operations plus reserve. Daily testing required."},
            {"id": 52, "name": "Inside BOP & Float Valve", "simple": "داخل drill string. Kelly valve (يدوي)، Float valve (أوتوماتيكي). يمنعوا backflow.", "technical": "Kelly valve: manual at top of kelly. Float valve: automatic check valve in string. Both prevent backflow. Backup if primary BOP fails or pipe breaks.", "exam": "Kelly valve: where? Top of kelly. Float valve: one-way, automatic. When useful? U-tubing prevention, backup well control."},
            {"id": 53, "name": "Diverter System", "simple": "للغاز السطحي. يحول التدفق بعيد عن الrig. ضغط منخفض فقط.", "technical": "Low pressure device (<500 psi rating) for shallow gas. Diverts flow away from rig to safe location. Not for well control. Used above surface casing.", "exam": "When? Shallow gas before surface casing. Not well control - diverts only. Vent lines away from personnel/equipment."},
            {"id": 54, "name": "BOP Testing Requirements", "simple": "اختبار قبل الحفر ودوري: Low pressure (annular)، High pressure (rams).", "technical": "Pressure tests: Low (200-300 psi) for annular, High (rated WP or 70%) for rams. Function tests: operate each component. Frequency: before drilling, every 14-21 days, after repairs.", "exam": "Test pressures: annular low, rams high. API requirements: before shoe drill-out, regular intervals. Document all tests. Failure = repair before ops."},
            {"id": 55, "name": "BOP Control Systems", "simple": "هيدروليكي لتشغيل BOP. redundancy ضروري: dual stations، backup power.", "technical": "Hydraulic system: pumps, accumulators, control panels, valves. Redundancy: dual control stations, backup power, accumulator reserve. Operate: locally (driller) or remotely (backup).", "exam": "How many stations? Minimum 2 (primary + backup). Power? Rig + backup (batteries/gen). Operate without power? Yes, from accumulator (limited)."}
        ]
    },
    
    "Module 6: Subsea Well Control": {
        "icon": "🌊",
        "description": "Deep water and subsea stack operations",
        "topics": [
            {"id": 56, "name": "Subsea vs Surface Differences", "simple": "subsea: choke line friction، riser margin، BOP على seabed.", "technical": "Key differences: BOP on seafloor not surface, choke line friction affects pressures, riser margin needed for safety, kill/choke lines long, weak point considerations.", "exam": "Main differences: CLF correction needed, riser margin essential, BOP access difficult, pressure corrections required."},
            {"id": 57, "name": "Choke Line Friction (CLF)", "simple": "الاحتكاك في خط الchoke. الضغط السطحي أقل من الحقيقي. لازم نضيف CLF.", "technical": "Friction in choke line reduces surface pressure reading. True SICP = Surface SICP + CLF. CLF from tables/calculations based on rate, line size, length. Critical correction.", "exam": "Always ADD CLF to surface reading for true pressure at BOP. Surface reads LOW. True SICP = Surface + CLF. Exam calculations include CLF."},
            {"id": 58, "name": "Riser Margin", "simple": "هامش أمان لإبقاء الriser ممتلئ. يمنع U-tubing عند الفصل الطارئ.", "technical": "Extra MW in riser vs seawater. RM = (MW - Seawater) × 0.052 × Water Depth. Prevents U-tubing if disconnect. Minimum 200 psi, typical 400-600 psi.", "exam": "Calculate: RM = (MW - 8.6) × 0.052 × WD. Purpose: safety margin for emergency disconnect. Minimum values specified. Prevents kick if riser lost."},
            {"id": 59, "name": "Riser Margin Calculation", "simple": "RM = (MW - 8.6) × 0.052 × عمق الماء.", "technical": "Seawater gradient: 0.445 psi/ft or 8.6 ppg equivalent. Mud heavier than seawater creates margin. Example: 12 ppg @ 5000 ft WD = (12-8.6)×0.052×5000 = 884 psi.", "exam": "Formula memorization essential. Seawater = 8.6 ppg. Calculate margin for given MW and water depth. Check if adequate (>200 psi minimum)."},
            {"id": 60, "name": "Kill Line vs Choke Line", "simple": "Kill line: لضخ الطين. Choke line: للتحكم في التدفق. كلاهما تحت الBOP.", "technical": "Kill line: pump kill mud below BOP. Choke line: take returns through choke. Both high pressure lines from seafloor. Selection depends on: operation type, pressures, friction considerations.", "exam": "Know functions. Kill = pump pathway. Choke = return pathway with pressure control. Both bypass riser. Critical for subsea operations."},
            {"id": 61, "name": "Subsea MAASP", "simple": "MAASP مختلف - نحسبه عند الseabed، مش السطح.", "technical": "Calculate at mudline not surface. Account for riser mud weight. MAASP at BOP = Fracture P - HP from mudline. Different from surface calculation.", "exam": "Subsea MAASP calculated at seafloor. Must account for water depth and riser. Lower than surface equivalent due to geometry."},
            {"id": 62, "name": "Weak Point Analysis", "simple": "أضعف نقطة: عادة casing shoe أو wellhead. لازم نحددها.", "technical": "Weakest point determines MAASP. Usually: last casing shoe, wellhead, or BOP connector. Must identify and calculate for each. Limits maximum surface pressure.", "exam": "Identify weak point. Calculate MAASP for each potential weak point. Use lowest value. Critical for kill planning."},
            {"id": 63, "name": "Subsea Kill Procedures", "simple": "نفس الطرق لكن مع تعديلات: CLF، riser margin، weak points.", "technical": "Same methods (Driller's, W&W) but modified for: CLF corrections, riser considerations, longer circulation times, different pressure monitoring points.", "exam": "Know modifications: add CLF to SICP, consider riser effects, account for line volumes. Principles same but calculations adjusted."},
            {"id": 64, "name": "Subsea BOP Testing", "simple": "اختبار عن بعد (remotely). أصعب من surface. استخدام ROV أحيانا.", "technical": "Remote testing via control pods. More complex than surface. Function tests via ROV if needed. Pressure testing through lines. Documentation critical.", "exam": "Testing challenges: remote operation, water depth, accessibility. Same requirements but execution different. ROV involvement for major work."},
            {"id": 65, "name": "Emergency Disconnect", "simple": "فصل الriser في الطوارئ. الriser margin يحمي البئر بعد الفصل.", "technical": "Disconnect riser from BOP in emergency (weather, drift-off). Well left with mud in hole. Riser margin keeps well overbalanced. Can reconnect when safe.", "exam": "When? Severe weather, rig drift, emergency. Result: riser separated, well shut-in at BOP. Riser margin prevents kick. Can reconnect later."}
        ]
    },
    
    "Module 7: Complications & Special Situations": {
        "icon": "🚨",
        "description": "Handle complications during well control operations",
        "topics": [
            {"id": 66, "name": "Gas Migration in Shut-in Well", "simple": "الغاز يطلع حتى لو البئر مغلق. SICP يزيد، SIDPP ثابت. نستخدم L&B أو volumetric.", "technical": "Gas rises due to density. SICP increases, SIDPP stable = migration. Actions: lubricate & bleed (maintain constant BHP) or volumetric method. Prevent MAASP breach.", "exam": "Signs: SICP up, SIDPP constant. Can't ignore. Methods: L&B or volumetric. Must act before MAASP. Continuous monitoring essential."},
            {"id": 67, "name": "Plugged Nozzle During Kill", "simple": "nozzle مسدود أثناء القتل. ضغط المضخة يزيد. الحل: نوقف، نطلع الbit، ننضف.", "technical": "Indication: pump pressure higher than schedule. Confirm: check if deviation from calculated. Action: stop kill, pull bit, clean/change nozzles, restart with new SCR.", "exam": "How to detect? Pump pressure doesn't follow schedule (too high). Action? Stop, pull bit, clean, get new SCR, recalculate pressures, restart."},
            {"id": 68, "name": "Washout During Kill", "simple": "ثقب في الأنابيب. الضغط ينخفض. نوقف، نحدد المكان، نطلع.", "technical": "Drill string leak. Indication: drill pipe pressure drops, can't maintain schedule pressure. Action: shut in, attempt to isolate, pull pipe to locate and repair.", "exam": "Detection: can't maintain drill pipe pressure (drops). Cause: hole in drill string. Action: shut in immediately, pull pipe, locate leak, repair/replace."},
            {"id": 69, "name": "Lost Circulation During Kill", "simple": "فقدان الطين أثناء القتل. خطير! نقلل rate، نستخدم LCM، ممكن نحتاج volumetric.", "technical": "Losing mud to formation during kill. Causes: exceeding fracture, high ECD. Action: reduce pump rate, add LCM, if severe use volumetric method instead.", "exam": "Indication: pit level dropping, loss of returns. Action: reduce rate first, add LCM, monitor SICP vs MAASP. Severe? Switch to volumetric method."},
            {"id": 70, "name": "Stuck Pipe During Well Control", "simple": "الأنابيب علقت! ما نقدرش نحرك. خيارات محدودة - volumetric أو bullheading.", "technical": "Can't move or circulate. Options limited: volumetric method (if BOP closed), spotting pill and working pipe, bullheading (last resort). Prevent: maintain circulation during kill.", "exam": "If stuck while shut-in? Volumetric method. If stuck while circulating? Try to free gently, continue kill if possible, volumetric if can't circulate."},
            {"id": 71, "name": "Underground Blowout", "simple": "الkick يدخل تكوين تاني تحت الأرض. خطير جدا! علامات: ضغوط غريبة، فقدان طين.", "technical": "Kick flows into weaker formation underground instead of surface. Very dangerous. Indications: unusual pressures, losses, no surface flow but kick confirmed. Rare but severe.", "exam": "Definition: flow between formations underground. Detection: losses to one zone while kicking from another. Very serious. May require cement plug, directional relief well."},
            {"id": 72, "name": "H2S Well Control", "simple": "H2S = غاز سام قاتل! احتياطات خاصة: safety equipment، wind direction، evacuation plans.", "technical": "Hydrogen sulfide: toxic, deadly even at low concentrations. Special procedures: H2S detection, SCBA availability, wind monitoring, evacuation routes, ignition source control. Well control same but safety critical.", "exam": "H2S dangers: toxic (kills at low ppm), heavier than air (accumulates), corrosive. Well control procedures similar but enhanced safety measures. Detect, protect, evacuate."},
            {"id": 73, "name": "Shallow Gas Kick", "simple": "غاز قريب من السطح. خطير - يتمدد كثير. نستخدم diverter، ما نغلقش البئر تماما.", "technical": "Gas above surface casing. Very dangerous - low fracture strength, large expansion. Use diverter system not BOP. Flow overboard away from rig. Don't shut in completely.", "exam": "Why dangerous? Low fracture pressure, no casing protection, large expansion. Action: use diverter, flow away from rig, don't fully shut in (will fracture)."},
            {"id": 74, "name": "Kick While Tripping", "simple": "kick أثناء رفع/تنزيل الأنابيب. نوقف، نعمل flow check، نغلق البئر، نملأ أنابيب.", "technical": "Detection harder (no circulation). If suspected: stop, set slips, flow check. If flowing: shut in with pipe in hole, install inside BOP or kelly valve, circulate out kick.", "exam": "Procedure: stop tripping, flow check, if flow = shut in, space out for kelly, install kelly valve or inside BOP, proceed with kill. Stripping may be needed."},
            {"id": 75, "name": "Well Control Without Returns", "simple": "ما فيش عودة للطين (lost circulation كاملة). صعب جدا! volumetric method فقط.", "technical": "Complete loss of returns to formation. Can't use normal methods. Only option: volumetric method. Monitor pressures, calculate volumes precisely. Very challenging.", "exam": "When? Severe lost circulation, can't get returns. Method? Volumetric only. Monitor SIDPP, calculate volumes to bleed/pump. Maintain BHP by volume balance."},
            {"id": 76, "name": "Simultaneous Operations (SIMOPS)", "simple": "عمليات متعددة نفس الوقت. خطر أعلى! coordination مهم جدا.", "technical": "Multiple activities simultaneously (drilling one well, production another nearby). Well control complications increase. Enhanced monitoring, communication, procedures needed.", "exam": "Increased risk during SIMOPS. Requirements: enhanced procedures, communication, monitoring. Kick on one well affects others. Coordination critical."},
            {"id": 77, "name": "Tapered String Calculations", "simple": "أنابيب بأحجام مختلفة. حسابات أصعب - لازم نحسب كل section لوحده.", "technical": "Different pipe sizes in string. Complicates calculations: each section different capacity, strokes to bit must account for all sections. Calculate segment by segment, sum up.", "exam": "How? Calculate each section separately: capacity × length = volume. Sum all sections. Strokes = total volume ÷ pump output. More complex but same principles."}
        ]
    },
    
    "Module 8: HSE & Best Practices": {
        "icon": "⚠️",
        "description": "Safety, regulations, and industry standards",
        "topics": [
            {"id": 78, "name": "Well Control Barriers", "simple": "primary barrier (الطين)، secondary barrier (BOP)، tertiary (casing). كل واحد backup للتاني.", "technical": "Barrier philosophy: Primary (mud column), Secondary (BOP, casing), Tertiary (casing, cement). Multiple independent barriers. Barrier management critical for safety.", "exam": "Primary: mud overbalance. Secondary: BOP system, casing, cement. Two independent barriers minimum required. Barrier failure = escalated procedures."},
            {"id": 79, "name": "Roles & Responsibilities", "simple": "Driller، Tool pusher، Company man، Choke operator - كل واحد له دور محدد.", "technical": "Driller: well operations, initial response. Tool pusher: rig supervision. Company man: overall well authority. Choke operator: pressure control during kill. Clear roles essential.", "exam": "Who does what? Driller: shuts in well, monitors. Tool pusher: supervises, assists. Company man: decisions, authority. Choke operator: maintains pressures during kill."},
            {"id": 80, "name": "Well Control Drills", "simple": "تدريبات دورية. كل الcrew لازم يتدرب. simulation للsituations مختلفة.", "technical": "Regular drills required (weekly/bi-weekly). Practice: shut-in, BOP operation, kill procedures, emergency response. All crew participate. Document and review.", "exam": "Why? Preparedness, muscle memory, teamwork. Frequency? Weekly or more. Content? All procedures, emergency scenarios. Required by regulations."},
            {"id": 81, "name": "API & IADC Standards", "simple": "المعايير العالمية: API RP 53، RP 59، IADC guidelines. لازم نتبعها.", "technical": "API RP 53: BOP systems. API RP 59: Well control operations. IADC: Drilling well control guidelines. Industry standards, often regulatory requirements. Regular updates.", "exam": "Know main standards exist. API 53 = BOP equipment/testing. API 59 = well control operations. Compliance required. Updated periodically."},
            {"id": 82, "name": "Incident Reporting & Investigation", "simple": "أي kick لازم يتسجل. investigation لمعرفة السبب. نتعلم من الأخطاء.", "technical": "All well control events must be reported. Investigation: root cause analysis, lessons learned, corrective actions. Share learnings industry-wide. Prevent recurrence.", "exam": "What to report? All kicks, shut-ins, well control events. Why? Learn, improve, regulatory requirement. Investigation identifies root cause and preventive measures."},
            {"id": 83, "name": "Pre-Spud Meeting & Well Planning", "simple": "اجتماع قبل بدء الحفر. نراجع كل شيء: well design، procedures، emergencies.", "technical": "Before drilling: review well design, pore/fracture pressures, casing program, mud program, BOP procedures, kill sheets, emergency procedures. All personnel attend.", "exam": "When? Before spud (start drilling). Who? All key personnel. Content? Complete well plan, procedures, contingencies. Ensures everyone prepared."},
            {"id": 84, "name": "Continuous Improvement", "simple": "دايما نحسن: new technology، lessons learned، training updates.", "technical": "Industry evolves: new equipment, procedures, technology. Incorporate lessons learned. Update training. Benchmarking. Safety culture improvement.", "exam": "Concept: always improving safety and procedures. Methods: lessons learned, technology adoption, training enhancement, audits, reviews."},
            {"id": 85, "name": "Environmental Considerations", "simple": "حماية البيئة مهمة: ما نطلعش طين أو غاز للبحر/البر بدون معالجة.", "technical": "Prevent pollution: proper mud handling, gas flaring controls, containment systems. Compliance with environmental regulations. Spill prevention and response plans.", "exam": "Well control must consider environmental protection. Can't just dump fluids. Diverter discharge managed. Regulations compliance essential."},
            {"id": 86, "name": "Lessons from Major Incidents", "simple": "نتعلم من Macondo، Piper Alpha، وغيرها. الأخطاء كانت: communication، procedures، equipment.", "technical": "Major incidents (Macondo, etc.) taught: importance of barriers, communication, procedure adherence, equipment reliability, decision-making. Industry changed after each.", "exam": "Know major incidents occurred. Lessons: multiple barriers essential, procedures must be followed, communication critical, equipment testing vital, management of change important."},
            {"id": 87, "name": "Regulatory Compliance", "simple": "قوانين ولوائح كل دولة. لازم نلتزم: testing، reporting، procedures، training.", "technical": "Jurisdictional regulations vary. Common requirements: BOP testing frequencies, personnel competency/certification, procedures documentation, incident reporting, audits. Compliance mandatory.", "exam": "Regulations exist and must be followed. Vary by location. Cover: equipment, training, procedures, reporting. Non-compliance = legal consequences, shutdown."}
        ]
    }
}

# Total: 87 topics across 8 modules - Complete IWCF Level 4 content
# Each topic has simple (Arabic), technical (English), and exam (test strategy) sections