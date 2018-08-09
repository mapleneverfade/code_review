INSERT INTO tmp_mgr_fat_mbl_first_page_channel_day
(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       -- 日期，           渠道，           授信客户数（获客数）
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案
	
	,7D_CRD_CUST_CNT         -- 近7日获客数
    ,7D_ADD_PRCP_BAL         -- 近7日净增 
	,7D_APL_CUST_CNT         -- 7天申请用户
	,7D_APV_PAS_CRD_CNT      -- 7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT -- 7天审批结案	                                           
);

INSERT INTO tmp_mgr_fat_mbl_first_page_channel_day
(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       -- 日期，           渠道，           授信客户数（获客数）
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案
	
	,7D_CRD_CUST_CNT         -- 近7日获客数
    ,7D_ADD_PRCP_BAL         -- 近7日净增 
	,7D_APL_CUST_CNT         -- 7天申请用户
	,7D_APV_PAS_CRD_CNT      -- 7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT -- 7天审批结案	                                           
);
INSERT INTO mgr_dim.page_channel_day
(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       -- 日期，           渠道，           授信客户数（获客数）
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案
	
	,7D_CRD_CUST_CNT         -- 近7日获客数
    ,7D_ADD_PRCP_BAL         -- 近7日净增 
	,7D_APL_CUST_CNT         -- 7天申请用户
	,7D_APV_PAS_CRD_CNT      -- 7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT -- 7天审批结案	                                           
);
INSERT INTO mgr_fat_mbl_first_page_channel_day
(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       -- 日期，           渠道，           授信客户数（获客数）
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案
	
	,7D_CRD_CUST_CNT         -- 近7日获客数
    ,7D_ADD_PRCP_BAL         -- 近7日净增 
	,7D_APL_CUST_CNT         -- 7天申请用户
	,7D_APV_PAS_CRD_CNT      -- 7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT -- 7天审批结案	                                           
);