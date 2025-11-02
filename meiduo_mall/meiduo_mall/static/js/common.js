/**
 * 获取指定名称的 Cookie
 * @param {string} name - Cookie 名称
 * @returns {string|undefined} Cookie 值（不存在则返回 undefined）
 */
const getCookie = (name) => {
    // 现代浏览器支持 document.cookie 直接拆分，用 String.prototype.matchAll 更严谨
    const cookieMatch = [...document.cookie.matchAll(new RegExp(`(^|;)\\s*${name}=([^;]+)`, 'g'))].pop();
    return cookieMatch ? cookieMatch[2] : undefined;
};

/**
 * 提取地址栏查询参数
 * @param {string} name - 参数名称
 * @returns {string|null} 参数值（不存在则返回 null，自动解码）
 */
const getQueryString = (name) => {
    // 现代 API：URLSearchParams 直接解析查询字符串，无需手动写正则
    const searchParams = new URLSearchParams(window.location.search);
    const value = searchParams.get(name);
    return value ? decodeURIComponent(value) : null;
};

/**
 * 生成 UUID v4（符合 RFC 4122 标准）
 * @returns {string} 标准 UUID v4 字符串
 */
const generateUUID = () => {
    // 现代浏览器支持 crypto API，生成更安全的随机数（替代 Math.random()）
    const crypto = window.crypto || window.msCrypto; // 兼容 IE 11
    if (!crypto) {
        // 降级方案：保留原时间戳逻辑（仅兼容旧环境，优先用 crypto）
        let d = Date.now();
        if (window.performance?.now) d += performance.now();
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }

    // 标准 UUID v4 生成逻辑（基于 crypto.getRandomValues）
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);
    // 版本位（第 6 个字节，设置为 0100，即版本 4）
    array[6] = (array[6] & 0x0f) | 0x40;
    // 变体位（第 8 个字节，设置为 10xx，即 RFC 4122 标准变体）
    array[8] = (array[8] & 0x3f) | 0x80;
    // 转换为十六进制字符串并添加分隔符
    return Array.from(array, (byte) => byte.toString(16).padStart(2, '0'))
        .join('')
        .replace(/^(.{8})(.{4})(.{4})(.{4})(.{12})$/, '$1-$2-$3-$4-$5');
};