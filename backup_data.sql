--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (permission_id, name) FROM stdin;
5d843596-93f7-4eae-92ba-7fc9b9a052f7	user:delete
69a45a70-93e0-4384-81b6-e2ac781a95b0	user:update
5e8bfc10-0e86-4719-af77-1bf947897025	permission:update
01526d73-4f5f-4d30-99cc-28233d462fdf	permission:delete
2e359263-b51c-49b1-ae85-92f222602303	permission:create
bef7f79a-1001-4f14-879d-4d13d09e56e2	role:create
1b9c739a-7a19-4ce1-8695-e3d1009310a4	role:update
bf3885c0-0239-4326-9071-7e825e631e83	role:delete
595080c3-8068-4125-a0e8-2ec7fd755bd9	role_permission:create
ee279d45-a024-4746-9a3e-9feef2621e79	role_permission:update
9f48c4db-56d1-4c30-acad-e6d12ee0329f	role_permission:delete
72f2a059-5f70-46ae-bec6-206618f4ad00	user:logout
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, name) FROM stdin;
c1bcd249-0df5-41d1-9230-ab9c92fabee7	user
bc0e2e90-d64e-4de0-9fed-e67d09e43793	admin
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
c1bcd249-0df5-41d1-9230-ab9c92fabee7	5d843596-93f7-4eae-92ba-7fc9b9a052f7
c1bcd249-0df5-41d1-9230-ab9c92fabee7	69a45a70-93e0-4384-81b6-e2ac781a95b0
bc0e2e90-d64e-4de0-9fed-e67d09e43793	69a45a70-93e0-4384-81b6-e2ac781a95b0
bc0e2e90-d64e-4de0-9fed-e67d09e43793	5d843596-93f7-4eae-92ba-7fc9b9a052f7
bc0e2e90-d64e-4de0-9fed-e67d09e43793	01526d73-4f5f-4d30-99cc-28233d462fdf
bc0e2e90-d64e-4de0-9fed-e67d09e43793	2e359263-b51c-49b1-ae85-92f222602303
bc0e2e90-d64e-4de0-9fed-e67d09e43793	5e8bfc10-0e86-4719-af77-1bf947897025
bc0e2e90-d64e-4de0-9fed-e67d09e43793	1b9c739a-7a19-4ce1-8695-e3d1009310a4
bc0e2e90-d64e-4de0-9fed-e67d09e43793	bf3885c0-0239-4326-9071-7e825e631e83
bc0e2e90-d64e-4de0-9fed-e67d09e43793	bef7f79a-1001-4f14-879d-4d13d09e56e2
bc0e2e90-d64e-4de0-9fed-e67d09e43793	595080c3-8068-4125-a0e8-2ec7fd755bd9
bc0e2e90-d64e-4de0-9fed-e67d09e43793	ee279d45-a024-4746-9a3e-9feef2621e79
bc0e2e90-d64e-4de0-9fed-e67d09e43793	9f48c4db-56d1-4c30-acad-e6d12ee0329f
c1bcd249-0df5-41d1-9230-ab9c92fabee7	72f2a059-5f70-46ae-bec6-206618f4ad00
bc0e2e90-d64e-4de0-9fed-e67d09e43793	72f2a059-5f70-46ae-bec6-206618f4ad00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, full_name, email, is_active, created_at, updated_at, password_hash, user_role_id) FROM stdin;
d3b20dc4-e819-42a7-b792-0fe99bbeff88	Admin Admin Admin	admin@gmail.com	t	2025-10-19 11:08:56.456646	2025-10-19 11:08:56.456646	$2b$12$kLvfyjKJ67paGk0yXhTPeOxW5CO9pAEeCfomI6QwodpixjQ2U6LkC	bc0e2e90-d64e-4de0-9fed-e67d09e43793
03fd7743-2b74-4b35-b213-c9655170c513	User User User	user@gmail.com	t	2025-10-19 11:09:30.39055	2025-10-19 11:09:30.39055	$2b$12$iv6bpJPTZiCcTrzr18dzku8acjVvLeoSsJTahhsNJgUMP2cLM9qhC	c1bcd249-0df5-41d1-9230-ab9c92fabee7
\.


--
-- PostgreSQL database dump complete
--

