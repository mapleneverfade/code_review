CREATE TABLE neo_fake.ceo_management_month(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
);

CREATE TABLE neo_fake.ceo_management_month(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
);


CREATE TABLE neo_fake.ceo_management_month(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
);

CREATE TABLE neo_fake.ceo_management_month(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
);


insert into tmp_mbl_first_page_channel_day
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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案
	
	, sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,distinct sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,distinct sum(apl_cust_cnt)           -- 7天申请用户数
	,distinct　sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
select * from mgr_fat.ceo_management_day;
select         * from ceo_management_month;
select 
      * from
	  cet;







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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案

	,distinct sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,distinct sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,distinct sum(apl_cust_cnt)           -- 7天申请用户数
	,distinct sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案

	,sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,sum(apl_cust_cnt)           -- 7天申请用户数
	,sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;


INSERT INTO mgr_fat.mbl_first_page_channel_day
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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案

	,sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,sum(apl_cust_cnt)           -- 7天申请用户数
	,sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
INSERT INTO mgr_fat.mbl_first_page_channel_day
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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案

	,sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,sum(apl_cust_cnt)           -- 7天申请用户数
	,sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
INSERT INTO mgr_fat.mbl_first_page_channel_day
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
)

select 
	 date'$v_date'           ,fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额,    复借贷款余额，   还款总金额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额,        净增余额,        逾期金额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   -- 申请用户数,      审批通过客户,    审批结案

	,sum(tdy_crd_cust_cnt)       -- 近7日获客数
	,sum(tdy_add_prcp_bal)       -- 近7日净增余额 
	,sum(apl_cust_cnt)           -- 7天申请用户数
	,sum(tdy_apv_pas_cust)       -- 7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   -- 7天审批结案数
	
from mgr_fat.ceo_management_day
where stat_dt > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
